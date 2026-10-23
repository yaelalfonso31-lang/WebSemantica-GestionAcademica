"""Acceso por rol, asignaciones reales, horarios, administración de grupos y seguridad.

Trabajan sobre una copia de tests/fixtures/xml (ver conftest.py): no usan ni modifican data/.
"""
from conftest import entrar


def html(r):
    return r.get_data(as_text=True)


# ───────────────────────────── login y seguridad ─────────────────────────────
def test_login_correcto_guarda_vinculo_con_el_registro(cliente):
    assert entrar(cliente, 'alumno').status_code == 302
    with cliente.session_transaction() as s:
        assert s['rol'] == 'alumno' and s['ref_id'] == 'A006'


def test_login_incorrecto_muestra_mensaje(cliente):
    r = entrar(cliente, 'alumno', 'mala')
    assert r.status_code == 200 and 'Credenciales incorrectas' in html(r)


def test_login_resiste_inyeccion_xpath(cliente):
    r = cliente.post('/login', data={'username': "x' or '1'='1", 'password': "x' or '1'='1"})
    assert r.status_code == 200
    with cliente.session_transaction() as s:
        assert 'user_id' not in s


def test_contrasenas_no_estan_en_claro(app):
    from app.services.xml_utils import cargar
    with app.app_context():
        for p in cargar('usuarios').xpath('//password'):
            assert p.text != '1234' and ':' in p.text


def test_api_sin_sesion_responde_401_json(cliente):
    r = cliente.get('/api/materias')
    assert r.status_code == 401 and r.get_json()['error']


def test_alumno_no_puede_borrar_ni_listar_alumnos(cliente):
    entrar(cliente, 'alumno')
    assert cliente.delete('/api/alumnos/A005').status_code == 403
    assert cliente.get('/api/alumnos').status_code == 403
    assert cliente.get('/grupos').status_code == 302
    assert cliente.post('/api/inscripciones', json={'alumno_id': 'A006', 'grupo_id': 'G-ICCS262-01'}).status_code == 403


def test_sparql_rechaza_rutas_fuera_de_la_carpeta(cliente):
    entrar(cliente, 'admin')
    assert cliente.post('/api/consultas/ejecutar', json={'archivo': '../config.py'}).status_code == 400
    assert cliente.post('/api/consultas/ejecutar', json={'archivo': 'alumnos_en_riesgo.rq'}).status_code == 200


# ───────────────────────────── alumno ─────────────────────────────
def test_kardex_muestra_nombres_estatus_y_orden_cronologico(cliente):
    entrar(cliente, 'alumno')
    t = html(cliente.get('/kardex'))
    assert 'Ensamblador' in t and 'Aprobado' in t and 'Reprobado' in t
    pos = [t.index(p) for p in ('Otoño 2026', 'Primavera 2026', 'Primavera 2025', 'Otoño 2024', 'Otoño 2023')]
    assert pos == sorted(pos)


def test_horario_del_alumno_es_semanal_y_sin_choques(cliente):
    entrar(cliente, 'alumno')
    t = html(cliente.get('/horarios'))
    assert 'Mi Horario Semanal' in t
    for materia in ('Sistemas Operativos II', 'Web Semántica', 'Inteligencia Artificial', 'Redes de Computadoras',
                    'Ingeniería de Software', 'Minería de Datos', 'Desarrollo de Aplicaciones Móviles'):
        assert materia in t
    assert 'Eduardo Profesor' in t
    assert 'semana__clase--choque' not in t.split('<style')[0].split('<tbody>', 1)[1]  # ninguna celda en choque
    assert '<span class="horario-resumen__value">7</span>' in t     # 7 clases


def test_panel_del_alumno_sugiere_materias_disponibles(cliente):
    entrar(cliente, 'alumno')
    t = html(cliente.get('/dashboard'))
    assert 'Materias que puedes cursar' in t and 'Probabilidad y Estadística' in t
    assert 'Sistemas Operativos II' not in t.split('Materias que puedes cursar')[1]   # esa ya la cursa


# ───────────────────────────── profesor ─────────────────────────────
def test_profesor_ve_solo_sus_ocho_grupos(cliente):
    entrar(cliente, 'profe')
    t = html(cliente.get('/mis_grupos'))
    for g in ('G-CCOS005-02', 'G-CCOS008-02', 'G-CCOS254-01', 'G-CCOS262-01', 'G-CCOS275-01',
              'G-ICCS256-02', 'G-ICCS257-02', 'G-ICCS258-02'):
        assert g in t
    assert 'G-ICCS257-01' not in t       # ese lo imparte otro profesor


def test_horario_del_profesor(cliente):
    entrar(cliente, 'profe')
    t = html(cliente.get('/horarios'))
    assert 'Clases que impartes' in t and 'Web Semántica' in t and '/calificar?grupo=G-CCOS275-01' in t
    assert '<span class="horario-resumen__value">8</span>' in t


def test_profesor_no_puede_calificar_grupo_ajeno(cliente):
    entrar(cliente, 'profe')
    assert cliente.get('/calificar?grupo=G-ICCS257-01').status_code == 302
    r = cliente.post('/api/calificar', json={'grupo': 'G-ICCS257-01', 'calificaciones': {'I031': '100'}})
    assert r.status_code == 403


def test_calificar_deriva_estatus_y_actualiza_promedio(cliente, app):
    from app.services.xml_utils import cargar
    entrar(cliente, 'profe')
    with app.app_context():
        insc = cargar('inscripciones').xpath("//inscripcion[alumno_id='A006' and grupo_id='G-CCOS254-01']")[0].get('id')
    r = cliente.post('/api/calificar', json={'grupo': 'G-CCOS254-01', 'calificaciones': {insc: '60'}})
    assert r.status_code == 200, r.get_json()
    with app.app_context():
        nodo = cargar('inscripciones').xpath('//inscripcion[@id=$i]', i=insc)[0]
        assert nodo.findtext('estatus') == 'Reprobado'
        assert [c.tag for c in nodo] == ['alumno_id', 'materia_id', 'grupo_id', 'periodo', 'calificacion_final', 'estatus']
        assert cargar('alumnos').xpath("//alumno[@id='A006']/promedio")[0].text == '82.3'   # (927.1 + 60) / 12
    bad = cliente.post('/api/calificar', json={'grupo': 'G-CCOS254-01', 'calificaciones': {insc: '150'}})
    assert bad.status_code == 400


# ───────────────────────────── administración de grupos ─────────────────────────────
def test_admin_ve_grupos_con_inscritos(cliente):
    entrar(cliente, 'admin')
    t = html(cliente.get('/grupos'))
    assert 'Grupos e Inscripciones' in t and 'G-CCOS275-01' in t and 'Nuevo grupo' in t


def test_crear_grupo_valida_traslapes_de_profesor_y_aula(cliente):
    entrar(cliente, 'admin')
    base = {'materia_id': 'ICCS004', 'profesor_id': 'P007', 'periodo': 'Otoño 2026', 'dia': 'Viernes',
            'hora_inicio': '15:00', 'hora_fin': '17:00', 'aula': 'Edificio 9 - Aula 1'}
    r = cliente.post('/api/grupos', json=base)
    assert r.status_code == 201 and r.get_json()['id'] == 'G-ICCS004-02'
    # P012 ya imparte los martes y jueves de 07:00 a 09:00
    r = cliente.post('/api/grupos', json={**base, 'profesor_id': 'P012', 'dia': 'Martes y Jueves',
                                          'hora_inicio': '08:00', 'hora_fin': '10:00', 'aula': 'Otra'})
    assert r.status_code == 400 and 'ya imparte' in r.get_json()['error']
    # misma aula que G-CCOS005-02 en su horario
    r = cliente.post('/api/grupos', json={**base, 'profesor_id': 'P007', 'dia': 'Martes y Jueves',
                                          'hora_inicio': '07:00', 'hora_fin': '09:00', 'aula': 'Edificio 1 - Aula 102'})
    assert r.status_code == 400 and 'aula' in r.get_json()['error'].lower()
    assert cliente.post('/api/grupos', json={**base, 'hora_fin': '14:00'}).status_code == 400   # fin antes que inicio
    assert cliente.post('/api/grupos', json={**base, 'materia_id': 'XXXX999'}).status_code == 400


def test_inscribir_valida_prerrequisitos_choques_y_duplicados(cliente):
    entrar(cliente, 'admin')
    r = cliente.post('/api/inscripciones', json={'alumno_id': 'A005', 'grupo_id': 'G-ICCS280-01'})
    assert r.status_code == 400 and 'Prerrequisitos' in r.get_json()['error']
    r = cliente.post('/api/inscripciones', json={'alumno_id': 'A001', 'grupo_id': 'G-ICCS260-01'})
    assert r.status_code == 400 and 'Choque de horario' in r.get_json()['error']
    r = cliente.post('/api/inscripciones', json={'alumno_id': 'A006', 'grupo_id': 'G-CCOS254-01'})
    assert r.status_code == 400 and 'en curso' in r.get_json()['error']
    r = cliente.post('/api/inscripciones', json={'alumno_id': 'A014', 'grupo_id': 'G-ICCS262-01'})
    assert r.status_code == 201, r.get_json()
    iid = r.get_json()['id']
    assert cliente.delete(f'/api/inscripciones/{iid}').status_code == 200
    assert cliente.delete('/api/inscripciones/I021').status_code == 409      # historial calificado: no se borra


# ───────────────────────────── integridad al eliminar ─────────────────────────────
def test_no_se_pueden_eliminar_registros_con_dependencias(cliente):
    entrar(cliente, 'admin')
    for url in ('/api/alumnos/A006', '/api/profesores/P012', '/api/materias/CCOS254', '/api/grupos/G-CCOS254-01'):
        r = cliente.delete(url)
        assert r.status_code == 409, url
        assert 'No se puede' in r.get_json()['error'] or 'inscripci' in r.get_json()['error']
    assert cliente.delete('/api/alumnos/A011').status_code == 200      # sin historial ni cuenta: sí


# ───────────────────────────── reglas y consultas ─────────────────────────────
def test_reglas_de_horarios():
    from app.services import asignaciones as A
    assert A.parsear_dias('Lunes y Miércoles') == ['Lunes', 'Miércoles']
    assert A.parsear_dias('lunes, miercoles y viernes') == ['Lunes', 'Miércoles', 'Viernes']
    a = {'periodo': 'P', 'dias': ['Lunes'], 'inicio': '07:00', 'fin': '09:00'}
    assert A.chocan(a, {**a, 'inicio': '08:00', 'fin': '10:00'})
    assert not A.chocan(a, {**a, 'inicio': '09:00', 'fin': '11:00'})        # contiguas no chocan
    assert not A.chocan(a, {**a, 'dias': ['Martes']})


def test_materias_disponibles_del_alumno(app):
    from app.services import asignaciones as A
    with app.app_context():
        ids = {m['id'] for m in A.materias_disponibles('A006')}
    assert {'ICCS260', 'ICCS262'} <= ids
    assert 'CCOS254' not in ids and 'CCOS005' not in ids        # en curso / ya aprobada


def test_nuevas_consultas_sparql(cliente):
    entrar(cliente, 'admin')
    def correr(q):
        r = cliente.post('/api/consultas/ejecutar', json={'archivo': q})
        assert r.status_code == 200, (q, r.get_json())
        return r.get_json()['data']
    disp = correr('materias_disponibles.rq')
    assert any(f['alumnoId'] == 'A006' and f['materiaId'] == 'ICCS260' for f in disp)
    pre = {(f['materiaId'], f['prerrequisitoId']): f['tipo'] for f in correr('prerrequisitos_de_materia.rq')}
    assert pre[('ICCS270', 'CCOS254')] == 'Directo' and pre[('ICCS270', 'CCOS252')] == 'Transitivo'
    assert correr('alumnos_por_materia.rq') and correr('profesores_por_departamento.rq')
    assert any(f['carrera'] == 'ICC' for f in correr('profesores_por_carrera.rq'))


def test_inscritos_de_un_grupo_son_solo_los_del_periodo_actual(app):
    """El historial de periodos anteriores no debe contarse como alumnos del grupo vigente."""
    from app.services import academic_metrics as M
    from app.services.xml_utils import cargar
    with app.app_context():
        g = cargar('grupos').xpath("//grupo[@id='G-CCOS005-02']")[0]
        ids = sorted(i.findtext('alumno_id') for i in M.inscripciones_de_grupo(g))
    assert ids == ['A001', 'A005']
