"""Acceso por rol, asignaciones reales de alumno/profesor y seguridad básica."""
from conftest import entrar


def html(r):
    return r.get_data(as_text=True)


# ───────── login ─────────
def test_login_correcto_guarda_vinculo_con_el_registro(cliente):
    r = entrar(cliente, 'alumno')
    assert r.status_code == 302
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
    for p in cargar('usuarios').xpath('//password'):
        assert p.text != '1234' and ':' in p.text


# ───────── alumno ─────────
def test_alumno_ve_su_kardex_con_nombres_de_materia(cliente):
    entrar(cliente, 'alumno')
    t = html(cliente.get('/kardex'))
    assert 'Ensamblador' in t and 'Aprobado' in t and 'Reprobado' in t


def test_alumno_ve_su_horario_con_profesor(cliente):
    entrar(cliente, 'alumno')
    t = html(cliente.get('/horarios'))
    assert 'G-ICCS258-02' in t and 'Eduardo Profesor' in t and 'G-ICCS257-01' in t


def test_dashboard_alumno_tiene_metricas(cliente):
    entrar(cliente, 'alumno')
    t = html(cliente.get('/dashboard'))
    assert 'Materias aprobadas' in t and 'Cursando ahora' in t


# ───────── profesor ─────────
def test_profesor_ve_solo_sus_grupos(cliente):
    entrar(cliente, 'profe')
    t = html(cliente.get('/mis_grupos'))
    assert 'G-ICCS258-02' in t and 'G-CCOS005-02' in t and 'G-ICCS257-01' not in t


def test_profesor_no_puede_calificar_grupo_ajeno(cliente):
    entrar(cliente, 'profe')
    r = cliente.get('/calificar?grupo=G-ICCS257-01')
    assert r.status_code == 302
    r = cliente.post('/api/calificar', json={'grupo': 'G-ICCS257-01', 'calificaciones': {'I001': '100'}})
    assert r.status_code == 403


def test_calificar_deriva_estatus_y_actualiza_promedio(cliente, app):
    from app.services.xml_utils import cargar
    entrar(cliente, 'profe')
    with app.app_context():
        insc = cargar('inscripciones').xpath(
            "//inscripcion[alumno_id='A006' and grupo_id='G-ICCS258-02']")[0].get('id')
    r = cliente.post('/api/calificar', json={'grupo': 'G-ICCS258-02', 'calificaciones': {insc: '60'}})
    assert r.status_code == 200, r.get_json()
    with app.app_context():
        nodo = cargar('inscripciones').xpath('//inscripcion[@id=$i]', i=insc)[0]
        assert nodo.findtext('estatus') == 'Reprobado'
        assert [c.tag for c in nodo] == ['alumno_id', 'materia_id', 'grupo_id', 'periodo', 'calificacion_final', 'estatus']
        assert cargar('alumnos').xpath("//alumno[@id='A006']/promedio")[0].text == '82.6'   # (849 + 60) / 11


# ───────── autorización de la API ─────────
def test_alumno_no_puede_borrar_ni_listar_alumnos(cliente):
    entrar(cliente, 'alumno')
    assert cliente.delete('/api/alumnos/A005').status_code == 403
    assert cliente.get('/api/alumnos').status_code == 403


def test_api_sin_sesion_responde_401_json(cliente):
    r = cliente.get('/api/materias')
    assert r.status_code == 401 and r.get_json()['error']


def test_sparql_rechaza_rutas_fuera_de_la_carpeta(cliente):
    entrar(cliente, 'admin')
    r = cliente.post('/api/consultas/ejecutar', json={'archivo': '../config.py'})
    assert r.status_code == 400
    assert cliente.post('/api/consultas/ejecutar', json={'archivo': 'alumnos_en_riesgo.rq'}).status_code == 200
