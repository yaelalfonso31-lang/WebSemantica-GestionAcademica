"""
Es la capa que une los XML entre sí 
(usuario -> alumno/profesor -> inscripciones -> grupos -> materias)
Las se usan rutas para no repetir XPath por todos lados.
"""
import copy
import re

from lxml import etree

from app.services import asignaciones as asig
from app.services.paths import ajuste
from app.services.xml_utils import cargar, texto, xpath


def indice_materias():
    out = {}
    for m in xpath(cargar('materias'), '//materia'):
        out[m.get('id')] = {
            'clave': m.get('clave', ''),
            'nombre': texto(m, 'nombre'),
            'creditos': int(texto(m, 'creditos', '0') or 0),
        }
    return out


def indice_profesores():
    return {p.get('id'): texto(p, 'nombre') for p in xpath(cargar('profesores'), '//profesor')}


def indice_alumnos():
    out = {}
    for a in xpath(cargar('alumnos'), '//alumno'):
        out[a.get('id')] = {
            'matricula': a.get('matricula', ''),
            'nombre': f"{texto(a, 'nombre')} {texto(a, 'apellidos')}".strip(),
        }
    return out


def orden_periodo(periodo):
    """'Otoño 2026' -> 20263. Permite ordenar cronológicamente (el texto se ordena mal)."""
    m = re.search(r'(\d{4})', periodo or '')
    anio = int(m.group(1)) if m else 0
    epoca = {'primavera': 1, 'verano': 2, 'otoño': 3, 'otono': 3}.get((periodo or '').split(' ')[0].lower(), 0)
    return anio * 10 + epoca


def _agregar(nodo, nombre, valor):
    etree.SubElement(nodo, nombre).text = str(valor)


#  reglas 
def estatus_por_calificacion(calificacion):
    """Una calificación determina el estatus: nadie puede 'aprobar' con 40."""
    return 'Aprobado' if calificacion >= ajuste('CALIFICACION_MINIMA') else 'Reprobado'


def parsear_calificacion(valor):
    """'' -> None (sin calificar). Lanza ValueError si está fuera de 0..ESCALA_MAX."""
    if valor is None or str(valor).strip() == '':
        return None
    try:
        cal = round(float(str(valor).strip()), 1)
    except ValueError:
        raise ValueError(f"'{valor}' no es un número válido.")
    if not 0 <= cal <= ajuste('ESCALA_MAX'):
        raise ValueError(f"La calificación debe estar entre 0 y {ajuste('ESCALA_MAX')}.")
    return cal


def promedio_de(alumno_id, inscripciones=None):
    """Promedio de las materias ya calificadas del alumno (None si no tiene ninguna)."""
    arbol = inscripciones if inscripciones is not None else cargar('inscripciones')
    notas = []
    for n in xpath(arbol, "//inscripcion[alumno_id=$a]/calificacion_final", a=alumno_id):
        if n.text and n.text.strip():
            notas.append(float(n.text))
    return round(sum(notas) / len(notas), 1) if notas else None


#  asignaciones del profesor 
def grupos_de_profesor(profesor_id):
    if not profesor_id:
        return []
    return xpath(cargar('grupos'), '//grupo[profesor_id=$p]', p=profesor_id)


def grupo_de_profesor(profesor_id, grupo_id):
    """El grupo solo si pertenece a ese profesor (control de propiedad)."""
    if not profesor_id or not grupo_id:
        return None
    r = xpath(cargar('grupos'), '//grupo[@id=$g and profesor_id=$p]', g=grupo_id, p=profesor_id)
    return r[0] if r else None


def inscripciones_de_grupo(grupo, inscripciones=None):
    """Inscripciones de un grupo. Las antiguas sin <grupo_id> se asignan por materia Y periodo
    (si no, el historial de periodos anteriores se contaría como alumnos del grupo actual)."""
    arbol = inscripciones if inscripciones is not None else cargar('inscripciones')
    return xpath(
        arbol,
        '//inscripcion[grupo_id=$g or (not(grupo_id) and materia_id=$m and periodo=$p)]',
        g=grupo.get('id'), m=texto(grupo, 'materia_id'), p=texto(grupo, 'periodo'))


def grupo_de_inscripcion(insc, grupos):
    gid = texto(insc, 'grupo_id')
    if gid:
        r = xpath(grupos, '//grupo[@id=$g]', g=gid)
        return r[0] if r else None
    r = xpath(grupos, '//grupo[materia_id=$m]', m=texto(insc, 'materia_id'))
    return r[0] if r else None


#  XML enriquecido para las vistas XSLT 
def xml_kardex(alumno_id):
    materias = indice_materias()
    raiz = etree.Element('inscripciones')
    for insc in xpath(cargar('inscripciones'), '//inscripcion[alumno_id=$a]', a=alumno_id):
        nodo = copy.deepcopy(insc)
        info = materias.get(texto(insc, 'materia_id'), {})
        _agregar(nodo, 'materia_nombre', info.get('nombre', ''))
        _agregar(nodo, 'creditos', info.get('creditos', 0))
        _agregar(nodo, 'orden_periodo', orden_periodo(texto(insc, 'periodo')))
        raiz.append(nodo)
    return etree.tostring(raiz, encoding='unicode')


def _grupos_del_alumno(alumno_id):
    grupos = cargar('grupos')
    vistos, out = set(), []
    for insc in xpath(cargar('inscripciones'), "//inscripcion[alumno_id=$a and estatus='Cursando']", a=alumno_id):
        g = grupo_de_inscripcion(insc, grupos)
        if g is not None and g.get('id') not in vistos:
            vistos.add(g.get('id'))
            out.append(g)
    return out


def _semana(grupos, alumnos_por_grupo=None):
    """Construye la cuadrícula semanal: franjas de 1 h x días, con celdas que abarcan varias filas."""
    materias, profesores = indice_materias(), indice_profesores()
    infos = [asig.info_grupo(g) for g in grupos]
    colores = {m: i % 8 for i, m in enumerate(sorted({i['materia'] for i in infos}))}
    usa_sabado = any('Sábado' in i['dias'] for i in infos)
    dias = asig.DIAS if usa_sabado else asig.DIAS[:5]
    raiz = etree.Element('semana')
    if not infos:
        return raiz
    h0 = min(asig.a_minutos(i['inicio']) // 60 for i in infos)
    h1 = max(-(-asig.a_minutos(i['fin']) // 60) for i in infos)  # techo
    raiz.set('inicio', f'{h0:02d}:00'); raiz.set('fin', f'{h1:02d}:00')
    for d in dias:
        etree.SubElement(raiz, 'dia').text = d
    celdas, tapadas = {}, set()
    for i in infos:
        ini, fin = asig.a_minutos(i['inicio']) // 60, -(-asig.a_minutos(i['fin']) // 60)
        for d in i['dias']:
            if d not in dias:
                continue
            if (d, ini) in celdas or any((d, h) in tapadas for h in range(ini, fin)):
                (celdas.get((d, ini)) or {}).update(choque='1')
                continue
            celdas[(d, ini)] = dict(filas=fin - ini, color=colores[i['materia']], grupo=i['id'], materia=i['materia'],
                                    materia_nombre=materias.get(i['materia'], {}).get('nombre', i['materia']),
                                    profesor_nombre=profesores.get(i['profesor'], ''), aula=i['aula'],
                                    inicio=i['inicio'], fin=i['fin'],
                                    alumnos=(alumnos_por_grupo or {}).get(i['id'], ''))
            tapadas.update((d, h) for h in range(ini + 1, fin))
    for h in range(h0, h1):
        f = etree.SubElement(raiz, 'franja', hora=f'{h:02d}:00')
        for d in dias:
            if (d, h) in tapadas:
                continue
            c = celdas.get((d, h))
            if c:
                etree.SubElement(f, 'celda', dia=d, tipo='clase', **{k: str(v) for k, v in c.items()})
            else:
                etree.SubElement(f, 'celda', dia=d, tipo='vacia')
    return raiz


def _horario_xml(rol, grupos, alumnos_por_grupo=None):
    materias, profesores = indice_materias(), indice_profesores()
    raiz = etree.Element('horario', rol=rol)
    horas, creditos_vistos = 0.0, {}
    for g in sorted(grupos, key=lambda x: (min(asig.DIAS.index(d) for d in asig.parsear_dias(texto(x, 'dia'))
                                              ) if asig.parsear_dias(texto(x, 'dia')) else 9, texto(x, 'hora_inicio'))):
        i = asig.info_grupo(g)
        dur = (asig.a_minutos(i['fin']) - asig.a_minutos(i['inicio'])) / 60
        horas += dur * len(i['dias'])
        nodo = copy.deepcopy(g)
        info = materias.get(i['materia'], {})
        creditos_vistos[i['materia']] = info.get('creditos', 0)
        _agregar(nodo, 'materia_nombre', info.get('nombre', ''))
        _agregar(nodo, 'profesor_nombre', profesores.get(i['profesor'], ''))
        _agregar(nodo, 'creditos', info.get('creditos', 0))
        _agregar(nodo, 'alumnos', (alumnos_por_grupo or {}).get(i['id'], ''))
        raiz.append(nodo)
    resumen = etree.SubElement(raiz, 'resumen')
    _agregar(resumen, 'clases', len(grupos))
    _agregar(resumen, 'horas', f'{horas:g}')
    _agregar(resumen, 'creditos', sum(creditos_vistos.values()))
    raiz.insert(0, _semana(grupos, alumnos_por_grupo))
    return etree.tostring(raiz, encoding='unicode')


def xml_horario(alumno_id):
    return _horario_xml('alumno', _grupos_del_alumno(alumno_id))


def xml_horario_profesor(profesor_id):
    grupos = grupos_de_profesor(profesor_id)
    inscripciones = cargar('inscripciones')
    conteo = {g.get('id'): len(inscripciones_de_grupo(g, inscripciones)) for g in grupos}
    return _horario_xml('profesor', grupos, conteo)


def xml_admin_grupos():
    """Todos los grupos con sus inscritos, más los catálogos que necesitan los formularios."""
    materias, profesores, alumnos = indice_materias(), indice_profesores(), indice_alumnos()
    inscripciones = cargar('inscripciones')
    raiz = etree.Element('grupos_admin', periodo=ajuste('PERIODO_ACTUAL'))
    cat = etree.SubElement(raiz, 'catalogos')
    for i, d in sorted(materias.items()):
        etree.SubElement(cat, 'materia', id=i).text = d['nombre']
    for i, n in sorted(profesores.items()):
        etree.SubElement(cat, 'profesor', id=i).text = n
    for a in xpath(cargar('alumnos'), "//alumno[estatus='Activo']"):
        etree.SubElement(cat, 'alumno', id=a.get('id'), matricula=a.get('matricula', '')).text = \
            alumnos.get(a.get('id'), {}).get('nombre', a.get('id'))
    grupos = sorted(xpath(cargar('grupos'), '//grupo'), key=lambda g: (texto(g, 'materia_id'), g.get('id')))
    for g in grupos:
        nodo = copy.deepcopy(g)
        _agregar(nodo, 'materia_nombre', materias.get(texto(g, 'materia_id'), {}).get('nombre', ''))
        _agregar(nodo, 'profesor_nombre', profesores.get(texto(g, 'profesor_id'), ''))
        lista = etree.SubElement(nodo, 'inscritos')
        for insc in inscripciones_de_grupo(g, inscripciones):
            al = alumnos.get(texto(insc, 'alumno_id'), {})
            etree.SubElement(lista, 'inscripcion', id=insc.get('id'), alumno_id=texto(insc, 'alumno_id'),
                             alumno=al.get('nombre', texto(insc, 'alumno_id')), matricula=al.get('matricula', ''),
                             estatus=texto(insc, 'estatus'), calificacion=texto(insc, 'calificacion_final'))
        raiz.append(nodo)
    return etree.tostring(raiz, encoding='unicode')


def xml_mis_grupos(profesor_id):
    materias = indice_materias()
    inscripciones = cargar('inscripciones')
    raiz = etree.Element('mis_grupos')
    for g in grupos_de_profesor(profesor_id):
        nodo = copy.deepcopy(g)
        insc = inscripciones_de_grupo(g, inscripciones)
        pendientes = [i for i in insc if not texto(i, 'calificacion_final')]
        _agregar(nodo, 'materia_nombre', materias.get(texto(g, 'materia_id'), {}).get('nombre', ''))
        _agregar(nodo, 'total_alumnos', len(insc))
        _agregar(nodo, 'pendientes', len(pendientes))
        raiz.append(nodo)
    return etree.tostring(raiz, encoding='unicode')


def xml_evaluacion(grupo):
    materias, alumnos = indice_materias(), indice_alumnos()
    mid = texto(grupo, 'materia_id')
    raiz = etree.Element('evaluacion', grupo=grupo.get('id'), materia=mid,
                         materia_nombre=materias.get(mid, {}).get('nombre', ''))
    for insc in inscripciones_de_grupo(grupo):
        nodo = copy.deepcopy(insc)
        al = alumnos.get(texto(insc, 'alumno_id'), {})
        _agregar(nodo, 'alumno_nombre', al.get('nombre', texto(insc, 'alumno_id')))
        _agregar(nodo, 'matricula', al.get('matricula', ''))
        raiz.append(nodo)
    return etree.tostring(raiz, encoding='unicode')


# ─────────────────────────── métricas de dashboards ──────────────────────────
def _dashboard(tipo, metricas, extra=None):
    raiz = etree.Element('dashboard')
    _agregar(raiz, 'tipo', tipo)
    cont = etree.SubElement(raiz, 'metricas')
    for nombre, valor in metricas:
        etree.SubElement(cont, 'metrica', nombre=nombre).text = str(valor)
    for nodo in (extra or []):
        raiz.append(nodo)
    return etree.tostring(raiz, encoding='unicode')


def xml_dashboard_admin():
    insc = cargar('inscripciones')
    alumnos = xpath(cargar('alumnos'), '//alumno')
    riesgo = [a for a in alumnos if float(texto(a, 'promedio', '0') or 0) < ajuste('UMBRAL_RIESGO')]
    promedios = [float(texto(a, 'promedio', '0') or 0) for a in alumnos]
    return _dashboard('administrativo', [
        ('Alumnos registrados', len(alumnos)),
        ('Profesores', len(xpath(cargar('profesores'), '//profesor'))),
        ('Materias en catálogo', len(xpath(cargar('materias'), '//materia'))),
        ('Grupos abiertos', len(xpath(cargar('grupos'), '//grupo'))),
        ('Inscripciones en curso', len(xpath(insc, "//inscripcion[estatus='Cursando']"))),
        ('Alumnos en riesgo', len(riesgo)),
        ('Promedio general', f"{sum(promedios) / len(promedios):.1f}" if promedios else '—'),
    ])


def _disponibles_xml(alumno_id):
    cont = etree.Element('disponibles')
    for m in asig.materias_disponibles(alumno_id)[:6]:
        etree.SubElement(cont, 'materia', id=m['id'], semestre=str(m['semestre']), creditos=str(m['creditos'])).text = m['nombre']
    return cont


def xml_dashboard_alumno(alumno_id):
    insc = cargar('inscripciones')
    materias = indice_materias()
    mias = xpath(insc, '//inscripcion[alumno_id=$a]', a=alumno_id)
    aprobadas = [i for i in mias if texto(i, 'estatus') == 'Aprobado']
    cursando = [i for i in mias if texto(i, 'estatus') == 'Cursando']
    prom = promedio_de(alumno_id, insc)
    creditos = sum(materias.get(texto(i, 'materia_id'), {}).get('creditos', 0) for i in aprobadas)
    return _dashboard('estudiante', [
        ('Promedio', f"{prom:.1f}" if prom is not None else '—'),
        ('Materias aprobadas', len(aprobadas)),
        ('Cursando ahora', len(cursando)),
        ('Créditos acumulados', creditos),
    ], [_disponibles_xml(alumno_id)])


def xml_dashboard_profesor(profesor_id):
    inscripciones = cargar('inscripciones')
    grupos = grupos_de_profesor(profesor_id)
    alumnos, pendientes = set(), 0
    for g in grupos:
        for i in inscripciones_de_grupo(g, inscripciones):
            alumnos.add(texto(i, 'alumno_id'))
            if not texto(i, 'calificacion_final'):
                pendientes += 1
    return _dashboard('docente', [
        ('Grupos asignados', len(grupos)),
        ('Alumnos a cargo', len(alumnos)),
        ('Calificaciones pendientes', pendientes),
    ])
