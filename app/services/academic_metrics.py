"""Reglas de negocio y consultas de apoyo: quién es quién y qué tiene asignado.

Es la capa que une los XML entre sí (usuario -> alumno/profesor -> inscripciones
-> grupos -> materias). Las rutas la usan para no repetir XPath por todos lados.
"""
import copy

from lxml import etree

from app.services.paths import ajuste
from app.services.xml_utils import cargar, texto, xpath


# ─────────────────────────── índices (id -> datos) ───────────────────────────
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


def _agregar(nodo, nombre, valor):
    etree.SubElement(nodo, nombre).text = str(valor)


# ─────────────────────────────── reglas ──────────────────────────────────────
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


# ───────────────────── asignaciones del profesor ─────────────────────────────
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
    """Inscripciones de un grupo. Las antiguas sin <grupo_id> se asignan por materia."""
    arbol = inscripciones if inscripciones is not None else cargar('inscripciones')
    return xpath(
        arbol,
        '//inscripcion[grupo_id=$g or (not(grupo_id) and materia_id=$m)]',
        g=grupo.get('id'), m=texto(grupo, 'materia_id'))


def grupo_de_inscripcion(insc, grupos):
    gid = texto(insc, 'grupo_id')
    if gid:
        r = xpath(grupos, '//grupo[@id=$g]', g=gid)
        return r[0] if r else None
    r = xpath(grupos, '//grupo[materia_id=$m]', m=texto(insc, 'materia_id'))
    return r[0] if r else None


# ───────────────────── XML enriquecido para las vistas XSLT ──────────────────
def xml_kardex(alumno_id):
    materias = indice_materias()
    raiz = etree.Element('inscripciones')
    for insc in xpath(cargar('inscripciones'), '//inscripcion[alumno_id=$a]', a=alumno_id):
        nodo = copy.deepcopy(insc)
        info = materias.get(texto(insc, 'materia_id'), {})
        _agregar(nodo, 'materia_nombre', info.get('nombre', ''))
        _agregar(nodo, 'creditos', info.get('creditos', 0))
        raiz.append(nodo)
    return etree.tostring(raiz, encoding='unicode')


def xml_horario(alumno_id):
    materias, profesores = indice_materias(), indice_profesores()
    grupos = cargar('grupos')
    raiz = etree.Element('horario_alumno')
    vistos = set()
    for insc in xpath(cargar('inscripciones'),
                      "//inscripcion[alumno_id=$a and estatus='Cursando']", a=alumno_id):
        g = grupo_de_inscripcion(insc, grupos)
        if g is None or g.get('id') in vistos:
            continue
        vistos.add(g.get('id'))
        nodo = copy.deepcopy(g)
        _agregar(nodo, 'materia_nombre', materias.get(texto(g, 'materia_id'), {}).get('nombre', ''))
        _agregar(nodo, 'profesor_nombre', profesores.get(texto(g, 'profesor_id'), ''))
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
def _dashboard(tipo, metricas):
    raiz = etree.Element('dashboard')
    _agregar(raiz, 'tipo', tipo)
    cont = etree.SubElement(raiz, 'metricas')
    for nombre, valor in metricas:
        etree.SubElement(cont, 'metrica', nombre=nombre).text = str(valor)
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
    ])


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
