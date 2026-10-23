"""Reglas para asignar: horarios, prerrequisitos, grupos e inscripciones.

Se usan tanto desde la interfaz de administración como desde scripts/ampliar_datos.py,
de modo que los datos de ejemplo cumplen exactamente las mismas reglas que el sistema.
Las funciones "problemas_*" nunca escriben: devuelven la lista de motivos por los que
una operación NO debe hacerse (lista vacía = todo bien).
"""
import re
import unicodedata

from lxml import etree

from app.services.paths import ajuste
from app.services.xml_utils import cargar, ruta_xml, texto, xpath

DIAS = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado']
_HORA = re.compile(r'^([01][0-9]|2[0-3]):[0-5][0-9]$')


def _plano(s):
    return unicodedata.normalize('NFKD', s or '').encode('ascii', 'ignore').decode().lower()


# ───────────────────────────── horarios ─────────────────────────────────────
def parsear_dias(dia_texto):
    """'Lunes y Miércoles' -> ['Lunes', 'Miércoles'] (en orden de semana)."""
    t = _plano(dia_texto)
    return [d for d in DIAS if _plano(d) in t]


def a_minutos(hhmm):
    h, m = hhmm.split(':')
    return int(h) * 60 + int(m)


def info_grupo(g):
    """Elemento <grupo> -> dict simple."""
    return {
        'id': g.get('id'), 'materia': texto(g, 'materia_id'), 'profesor': texto(g, 'profesor_id'),
        'periodo': texto(g, 'periodo'), 'dias': parsear_dias(texto(g, 'dia')),
        'dia_texto': texto(g, 'dia'), 'inicio': texto(g, 'hora_inicio'), 'fin': texto(g, 'hora_fin'),
        'aula': texto(g, 'aula'),
    }


def chocan(a, b):
    """¿Dos grupos (dicts de info_grupo) coinciden en algún día y se traslapan sus horas?"""
    if a['periodo'] != b['periodo'] or not set(a['dias']) & set(b['dias']):
        return False
    return a_minutos(a['inicio']) < a_minutos(b['fin']) and a_minutos(b['inicio']) < a_minutos(a['fin'])


# ───────────────────────────── grupos ───────────────────────────────────────
def siguiente_id_grupo(materia_id, grupos=None):
    grupos = grupos if grupos is not None else cargar('grupos')
    usados = [int(m.group(1)) for g in xpath(grupos, '//grupo[materia_id=$m]', m=materia_id)
              if (m := re.search(r'-(\d{2})$', g.get('id', '')))]
    return f'G-{materia_id}-{(max(usados) + 1) if usados else 1:02d}'


def problemas_grupo(d, grupos=None, materias=None, profesores=None):
    """d = {materia_id, profesor_id, periodo, dia, hora_inicio, hora_fin, aula}."""
    grupos = grupos if grupos is not None else cargar('grupos')
    materias = materias if materias is not None else cargar('materias')
    profesores = profesores if profesores is not None else cargar('profesores')
    p = []
    if not xpath(materias, '//materia[@id=$m]', m=d.get('materia_id', '')):
        p.append(f"La materia '{d.get('materia_id', '')}' no existe en el catálogo.")
    if not xpath(profesores, '//profesor[@id=$x]', x=d.get('profesor_id', '')):
        p.append(f"El profesor '{d.get('profesor_id', '')}' no existe.")
    if not d.get('periodo', '').strip():
        p.append('Falta el periodo.')
    if not d.get('aula', '').strip():
        p.append('Falta el aula.')
    dias = parsear_dias(d.get('dia', ''))
    if not dias:
        p.append("Indica al menos un día válido (por ejemplo 'Lunes y Miércoles').")
    ini, fin = d.get('hora_inicio', ''), d.get('hora_fin', '')
    if not (_HORA.match(ini) and _HORA.match(fin)):
        p.append('Las horas deben tener formato HH:MM (por ejemplo 07:00).')
    elif a_minutos(fin) <= a_minutos(ini):
        p.append('La hora de fin debe ser posterior a la de inicio.')
    if p:
        return p
    nuevo = {'id': d.get('id', ''), 'periodo': d['periodo'], 'dias': dias, 'inicio': ini, 'fin': fin}
    for g in xpath(grupos, '//grupo'):
        otro = info_grupo(g)
        if otro['id'] == d.get('id') or not chocan(nuevo, otro):
            continue
        if otro['profesor'] == d['profesor_id']:
            p.append(f"El profesor ya imparte {otro['id']} en ese horario.")
        if _plano(otro['aula']) == _plano(d['aula']):
            p.append(f"El aula '{d['aula']}' ya está ocupada por {otro['id']} en ese horario.")
    return p


def crear_grupo(d):
    """Valida, agrega y guarda un grupo. Devuelve el id nuevo; lanza ValueError con los motivos."""
    from app.services.xml_repository import LOCK_ESCRITURA, XMLRepository
    with LOCK_ESCRITURA:
        grupos = cargar('grupos')
        problemas = problemas_grupo(d, grupos)
        if problemas:
            raise ValueError(' '.join(problemas))
        gid = d.get('id') or siguiente_id_grupo(d['materia_id'], grupos)
        if xpath(grupos, '//grupo[@id=$g]', g=gid):
            raise ValueError(f'Ya existe el grupo {gid}.')
        g = etree.SubElement(grupos.getroot(), 'grupo', id=gid)
        for tag in ('materia_id', 'profesor_id', 'periodo', 'dia', 'hora_inicio', 'hora_fin', 'aula'):
            etree.SubElement(g, tag).text = d[tag].strip()
        XMLRepository('grupos')._guardar_xml(grupos, ruta_xml('grupos'), reconstruir_grafo=False)
    return gid


def problemas_eliminar_grupo(grupo_id):
    n = len(xpath(cargar('inscripciones'), '//inscripcion[grupo_id=$g]', g=grupo_id))
    return [f'El grupo {grupo_id} tiene {n} inscripción(es). Da de baja a esos alumnos antes de eliminarlo.'] if n else []


# ─────────────────────────── inscripciones ──────────────────────────────────
def siguiente_id_inscripcion(inscripciones=None):
    insc = inscripciones if inscripciones is not None else cargar('inscripciones')
    nums = [int(m.group(1)) for i in xpath(insc, '//inscripcion') if (m := re.search(r'(\d+)$', i.get('id', '')))]
    return f'I{(max(nums) + 1) if nums else 1:03d}'


def aprobadas(alumno_id, inscripciones=None):
    insc = inscripciones if inscripciones is not None else cargar('inscripciones')
    return {texto(i, 'materia_id') for i in
            xpath(insc, "//inscripcion[alumno_id=$a and estatus='Aprobado']", a=alumno_id)}


def prerrequisitos_de(materia_id, materias=None):
    materias = materias if materias is not None else cargar('materias')
    return [p.get('ref') for p in xpath(materias, '//materia[@id=$m]/prerrequisitos/prerrequisito', m=materia_id)]


def problemas_inscripcion(alumno_id, grupo_id, alumnos=None, grupos=None, inscripciones=None, materias=None):
    alumnos = alumnos if alumnos is not None else cargar('alumnos')
    grupos = grupos if grupos is not None else cargar('grupos')
    inscripciones = inscripciones if inscripciones is not None else cargar('inscripciones')
    materias = materias if materias is not None else cargar('materias')

    al = xpath(alumnos, '//alumno[@id=$a]', a=alumno_id)
    gr = xpath(grupos, '//grupo[@id=$g]', g=grupo_id)
    if not al:
        return [f"El alumno '{alumno_id}' no existe."]
    if not gr:
        return [f"El grupo '{grupo_id}' no existe."]
    p = []
    if texto(al[0], 'estatus') != 'Activo':
        p.append(f"El alumno no está activo (estatus: {texto(al[0], 'estatus')}).")
    g = info_grupo(gr[0])
    mias = xpath(inscripciones, '//inscripcion[alumno_id=$a]', a=alumno_id)
    for i in mias:
        if texto(i, 'materia_id') == g['materia'] and texto(i, 'estatus') in ('Cursando', 'Aprobado'):
            p.append('La materia ya está ' + ('aprobada.' if texto(i, 'estatus') == 'Aprobado' else 'en curso.'))
            break
    ya = aprobadas(alumno_id, inscripciones)
    faltan = [r for r in prerrequisitos_de(g['materia'], materias) if r not in ya]
    if faltan:
        p.append('Prerrequisitos sin aprobar: ' + ', '.join(faltan) + '.')
    for i in mias:
        if texto(i, 'estatus') != 'Cursando' or not texto(i, 'grupo_id'):
            continue
        otro = xpath(grupos, '//grupo[@id=$g]', g=texto(i, 'grupo_id'))
        if otro and chocan(g, info_grupo(otro[0])):
            p.append(f"Choque de horario con {texto(i, 'grupo_id')} ({info_grupo(otro[0])['dia_texto']} "
                     f"{info_grupo(otro[0])['inicio']}-{info_grupo(otro[0])['fin']}).")
    return p


def inscribir(alumno_id, grupo_id):
    """Inscribe al alumno en el grupo. Devuelve el id de la inscripción; ValueError con los motivos."""
    from app.services.xml_repository import LOCK_ESCRITURA, XMLRepository
    with LOCK_ESCRITURA:
        insc = cargar('inscripciones')
        problemas = problemas_inscripcion(alumno_id, grupo_id, inscripciones=insc)
        if problemas:
            raise ValueError(' '.join(problemas))
        g = xpath(cargar('grupos'), '//grupo[@id=$g]', g=grupo_id)[0]
        iid = siguiente_id_inscripcion(insc)
        n = etree.SubElement(insc.getroot(), 'inscripcion', id=iid)
        etree.SubElement(n, 'alumno_id').text = alumno_id
        etree.SubElement(n, 'materia_id').text = texto(g, 'materia_id')
        etree.SubElement(n, 'grupo_id').text = grupo_id
        etree.SubElement(n, 'periodo').text = texto(g, 'periodo')
        etree.SubElement(n, 'estatus').text = 'Cursando'
        XMLRepository('inscripciones')._guardar_xml(insc, ruta_xml('inscripciones'))
    return iid


def dar_de_baja(inscripcion_id):
    """Elimina una inscripción en curso (no se permite borrar historial calificado)."""
    from app.services.xml_repository import LOCK_ESCRITURA, XMLRepository
    with LOCK_ESCRITURA:
        insc = cargar('inscripciones')
        n = xpath(insc, '//inscripcion[@id=$i]', i=inscripcion_id)
        if not n:
            raise ValueError(f"La inscripción '{inscripcion_id}' no existe.")
        if texto(n[0], 'estatus') != 'Cursando':
            raise ValueError('Solo se pueden dar de baja inscripciones en curso; el historial calificado se conserva.')
        n[0].getparent().remove(n[0])
        XMLRepository('inscripciones')._guardar_xml(insc, ruta_xml('inscripciones'))


# ──────────────────── materias que el alumno puede cursar ───────────────────
def materias_disponibles(alumno_id):
    """Materias no aprobadas ni en curso cuyos prerrequisitos ya están aprobados."""
    materias, insc = cargar('materias'), cargar('inscripciones')
    ya = aprobadas(alumno_id, insc)
    cursando = {texto(i, 'materia_id') for i in
                xpath(insc, "//inscripcion[alumno_id=$a and estatus='Cursando']", a=alumno_id)}
    out = []
    for m in xpath(materias, '//materia'):
        mid = m.get('id')
        if mid in ya or mid in cursando:
            continue
        if all(p.get('ref') in ya for p in m.xpath('prerrequisitos/prerrequisito')):
            out.append({'id': mid, 'nombre': texto(m, 'nombre'), 'semestre': int(texto(m, 'semestre', '0') or 0),
                        'creditos': int(texto(m, 'creditos', '0') or 0)})
    return sorted(out, key=lambda x: (x['semestre'], x['id']))


# ───────────────────── integridad al eliminar registros ─────────────────────
def _cuentas_con_ref(ref):
    return [texto(u, 'username') for u in xpath(cargar('usuarios'), '//usuario[ref=$r]', r=ref)]


def problemas_eliminar_alumno(alumno_id):
    insc = xpath(cargar('inscripciones'), '//inscripcion[alumno_id=$a]', a=alumno_id)
    p = []
    if insc:
        en_curso = sum(1 for i in insc if texto(i, 'estatus') == 'Cursando')
        p.append(f"Tiene {len(insc)} inscripción(es) en su historial ({en_curso} en curso). "
                 "Para conservar el historial cambia su estatus a 'Baja' en lugar de eliminarlo.")
    cuentas = _cuentas_con_ref(alumno_id)
    if cuentas:
        p.append('Tiene una cuenta de usuario vinculada: ' + ', '.join(cuentas) + '.')
    return p


def problemas_eliminar_profesor(profesor_id):
    p = []
    grupos = [g.get('id') for g in xpath(cargar('grupos'), '//grupo[profesor_id=$p]', p=profesor_id)]
    if grupos:
        p.append(f"Imparte {len(grupos)} grupo(s): {', '.join(grupos)}. Reasígnalos o elimínalos primero.")
    titular = xpath(cargar('materias'), '//materia[profesor/@id=$p]/@id', p=profesor_id)
    if titular:
        p.append(f"Es titular de {len(titular)} materia(s): {', '.join(titular)}.")
    cuentas = _cuentas_con_ref(profesor_id)
    if cuentas:
        p.append('Tiene una cuenta de usuario vinculada: ' + ', '.join(cuentas) + '.')
    return p


def problemas_eliminar_materia(materia_id):
    p = []
    grupos = [g.get('id') for g in xpath(cargar('grupos'), '//grupo[materia_id=$m]', m=materia_id)]
    if grupos:
        p.append(f"Tiene {len(grupos)} grupo(s): {', '.join(grupos)}.")
    n = len(xpath(cargar('inscripciones'), '//inscripcion[materia_id=$m]', m=materia_id))
    if n:
        p.append(f'Está en {n} inscripción(es) del historial académico.')
    return p


def eliminar_grupo(grupo_id):
    from app.services.xml_repository import LOCK_ESCRITURA, XMLRepository
    with LOCK_ESCRITURA:
        grupos = cargar('grupos')
        n = xpath(grupos, '//grupo[@id=$g]', g=grupo_id)
        if not n:
            raise ValueError(f"El grupo '{grupo_id}' no existe.")
        problemas = problemas_eliminar_grupo(grupo_id)
        if problemas:
            raise ValueError(' '.join(problemas))
        n[0].getparent().remove(n[0])
        XMLRepository('grupos')._guardar_xml(grupos, ruta_xml('grupos'), reconstruir_grafo=False)
