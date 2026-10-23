"""Amplía los datos de ejemplo SIN borrar ni modificar lo que ya existe.

    python scripts/ampliar_datos.py             # aplica los cambios
    python scripts/ampliar_datos.py --dry-run   # solo muestra qué haría

- Agrega únicamente lo que falta (por ID): materias, profesores, alumnos, grupos e inscripciones.
- Cada grupo y cada inscripción se valida con las mismas reglas que usa el sistema
  (prerrequisitos, choques de horario de alumno/profesor/aula, materia ya aprobada...).
  Lo que no cumple se omite y se informa el motivo.
- Los profesores y alumnos nuevos son datos ficticios de ejemplo. Los respaldos de lo que se
  reescribe quedan en data/backups/.
"""
import os
import sys
import unicodedata
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from lxml import etree  # noqa: E402

import config  # noqa: E402
from app.services import asignaciones as A  # noqa: E402
from app.services.rdf_graph import SemanticEngine  # noqa: E402
from app.services.xml_repository import XMLRepository  # noqa: E402
from app.services.xml_utils import ruta_xml, texto  # noqa: E402

DRY = '--dry-run' in sys.argv
PERIODO = config.PERIODO_ACTUAL
PARSER = etree.XMLParser(remove_blank_text=True)
informe = {'agregado': [], 'omitido': []}


def cargar(e):
    return etree.parse(ruta_xml(e), PARSER)


def guardar(arbol, entidad, grafo=False):
    if not DRY:
        XMLRepository(entidad)._guardar_xml(arbol, ruta_xml(entidad), reconstruir_grafo=grafo)


def slug(t):
    s = unicodedata.normalize('NFKD', t).encode('ascii', 'ignore').decode()
    return re.sub(r'[^a-z0-9]+', '.', s.lower()).strip('.')


def sub(padre, tag, txt=None, **at):
    e = etree.SubElement(padre, tag, **at)
    if txt is not None:
        e.text = str(txt)
    return e


# ═════════════════════════════ DEFINICIONES ═════════════════════════════════
# (id, nombre, descripción, créditos, semestre, profesor_id, [prerrequisitos])
MATERIAS = [
    ('CCOS254', 'Sistemas Operativos II', 'Planificación avanzada, memoria virtual, sistemas de archivos y concurrencia.', 6, 5, 'P012', ['CCOS252']),
    ('CCOS260', 'Redes de Computadoras', 'Modelos de capas, protocolos TCP/IP, direccionamiento y enrutamiento.', 6, 5, 'P013', ['CCOS252']),
    ('ICCS260', 'Probabilidad y Estadística', 'Variables aleatorias, distribuciones e inferencia estadística básica.', 6, 4, 'P002', ['CCOS008']),
    ('CCOS262', 'Ingeniería de Software', 'Ciclo de vida del software, requisitos, diseño, pruebas y metodologías ágiles.', 6, 6, 'P012', ['CCOS013']),
    ('ICCS262', 'Compiladores', 'Análisis léxico, sintáctico y semántico; generación de código.', 6, 6, 'P003', ['CCOS005', 'CCOS013']),
    ('CCOS270', 'Inteligencia Artificial', 'Búsqueda, representación del conocimiento y aprendizaje automático.', 6, 7, 'P014', ['CCOS013', 'ICCS256']),
    ('CCOS280', 'Seguridad Informática', 'Criptografía aplicada, seguridad en redes y en aplicaciones.', 6, 7, 'P013', ['CCOS260']),
    ('ICCS280', 'Desarrollo de Aplicaciones Móviles', 'Diseño y construcción de aplicaciones para dispositivos móviles.', 6, 7, 'P015', ['ICCS258']),
    ('CCOS275', 'Web Semántica', 'RDF, ontologías OWL, consultas SPARQL y datos enlazados.', 6, 8, 'P012', ['ICCS256', 'ICCS258']),
    ('ICCS270', 'Computación en la Nube', 'Virtualización, servicios en la nube, contenedores y despliegue escalable.', 6, 8, 'P014', ['CCOS254', 'CCOS260']),
]
PROFESORES = [  # datos ficticios de ejemplo
    ('P013', 'Mariana Solís-Vega', 'Redes y Seguridad'),
    ('P014', 'Ricardo Ochoa-Barrios', 'Inteligencia Artificial'),
    ('P015', 'Daniela Fuentes-Rojas', 'Desarrollo de Software Móvil'),
]
# (matrícula, id, nombre, apellidos, carrera, semestre)
ALUMNOS = [
    ('A006', '202254021', 'Yael Alfonso', 'Serrano Pastrana', 'C001', 8),
    ('A007', '20230007', 'Diego', 'Ramírez Soto', 'C001', 6),
    ('A008', '20230008', 'Ana Sofía', 'Mendoza Cruz', 'C001', 5),
    ('A009', '20240009', 'Luis Ángel', 'Torres Vega', 'C001', 4),
    ('A010', '20240010', 'Fernanda', 'Ortiz Lara', 'C001', 4),
    ('A012', '20220012', 'Jorge', 'Castillo Pérez', 'C001', 8),
    ('A013', '20230013', 'Valeria', 'Núñez Ibarra', 'C001', 5),
    ('A014', '20220014', 'Miguel Ángel', 'Reyes Salas', 'C001', 7),
    ('A015', '20240015', 'Paola', 'Guzmán Herrera', 'C001', 3),
]
LM, MJ, V = 'Lunes y Miércoles', 'Martes y Jueves', 'Viernes'
# (materia, profesor, días, inicio, fin, aula)  -> el id se genera (G-MATERIA-NN)
GRUPOS = [
    ('CCOS008', 'P012', LM, '07:00', '09:00', 'Edificio 1 - Aula 103'),
    ('ICCS257', 'P012', V, '09:00', '12:00', 'Laboratorio de Cómputo A'),
    ('CCOS262', 'P012', MJ, '11:00', '13:00', 'Edificio 2 - Aula 204'),
    ('CCOS254', 'P012', LM, '13:00', '15:00', 'Laboratorio de Cómputo A'),
    ('CCOS275', 'P012', LM, '15:00', '17:00', 'Laboratorio de Cómputo A'),
    ('CCOS260', 'P013', MJ, '13:00', '15:00', 'Edificio 2 - Aula 203'),
    ('CCOS280', 'P013', LM, '11:00', '13:00', 'Edificio 3 - Aula 302'),
    ('CCOS270', 'P014', LM, '09:00', '11:00', 'Edificio 3 - Aula 301'),
    ('ICCS270', 'P014', MJ, '17:00', '19:00', 'Edificio 3 - Aula 301'),
    ('ICCS280', 'P015', LM, '17:00', '19:00', 'Laboratorio de Cómputo C'),
    ('ICCS260', 'P002', MJ, '07:00', '09:00', 'Edificio 1 - Aula 105'),
    ('ICCS262', 'P003', V, '12:00', '15:00', 'Edificio 3 - Aula 303'),
]
# Historial (materia, periodo, calificación) — sin grupo; se valida contra prerrequisitos
HIST = {
    'A006': [],  # el historial de Yael ya existe en inscripciones.xml
    'A007': [('CCOS005', 'Otoño 2024', 88), ('CCOS008', 'Otoño 2024', 91), ('CCOS013', 'Primavera 2025', 84), ('ICCS004', 'Primavera 2025', 77),
             ('CCOS252', 'Otoño 2025', 80), ('ICCS007', 'Otoño 2025', 82), ('ICCS006', 'Primavera 2026', 86)],
    'A008': [('CCOS005', 'Primavera 2025', 93), ('CCOS008', 'Primavera 2025', 89), ('CCOS013', 'Otoño 2025', 90), ('ICCS004', 'Otoño 2025', 85)],
    'A009': [('CCOS005', 'Otoño 2025', 72), ('CCOS008', 'Otoño 2025', 70), ('ICCS004', 'Primavera 2026', 68)],
    'A010': [('CCOS005', 'Primavera 2026', 90), ('CCOS008', 'Primavera 2026', 87)],
    'A012': [('CCOS005', 'Otoño 2022', 85), ('CCOS008', 'Otoño 2022', 82), ('CCOS013', 'Primavera 2023', 79), ('ICCS004', 'Primavera 2023', 75),
             ('CCOS252', 'Otoño 2023', 83), ('ICCS007', 'Otoño 2023', 78), ('ICCS250', 'Primavera 2024', 81), ('ICCS256', 'Primavera 2024', 88),
             ('ICCS006', 'Otoño 2024', 76), ('CCOS254', 'Primavera 2025', 84), ('ICCS258', 'Primavera 2026', 80)],
    'A013': [('CCOS005', 'Otoño 2024', 70), ('CCOS008', 'Otoño 2024', 71), ('CCOS013', 'Primavera 2025', 65), ('CCOS013', 'Otoño 2025', 73)],
    'A014': [('CCOS005', 'Primavera 2024', 95), ('CCOS008', 'Primavera 2024', 92), ('CCOS013', 'Otoño 2024', 94), ('ICCS004', 'Otoño 2024', 90),
             ('CCOS252', 'Primavera 2025', 91), ('ICCS256', 'Primavera 2025', 93), ('ICCS007', 'Primavera 2025', 88), ('ICCS250', 'Otoño 2025', 92),
             ('CCOS254', 'Otoño 2025', 90), ('CCOS260', 'Primavera 2026', 89), ('ICCS258', 'Primavera 2026', 94)],
    'A015': [('CCOS005', 'Primavera 2026', 85), ('ICCS004', 'Primavera 2026', 88)],
}
# Inscripciones del periodo actual (alumno -> grupos). Se intenta en orden y se omite lo inválido.
ACTUAL = {
    'A006': ['G-CCOS254-01', 'G-CCOS262-01', 'G-CCOS260-01', 'G-CCOS270-01', 'G-CCOS275-01', 'G-ICCS280-01'],
    'A002': ['G-CCOS254-01', 'G-CCOS262-01', 'G-ICCS260-01', 'G-ICCS262-01'],
    'A003': ['G-CCOS262-01'],
    'A007': ['G-CCOS254-01', 'G-ICCS250-01', 'G-ICCS256-02', 'G-ICCS257-02', 'G-ICCS258-02'],
    'A008': ['G-CCOS252-01', 'G-ICCS007-01', 'G-ICCS006-01', 'G-ICCS256-02', 'G-ICCS258-01'],
    'A009': ['G-CCOS013-01', 'G-ICCS004-01', 'G-ICCS006-01'],
    'A010': ['G-CCOS013-01', 'G-ICCS004-01', 'G-ICCS006-01', 'G-ICCS257-01'],
    'A012': ['G-CCOS260-01', 'G-CCOS262-01', 'G-CCOS275-01', 'G-CCOS270-01'],
    'A013': ['G-CCOS252-01', 'G-ICCS004-01', 'G-ICCS257-02', 'G-ICCS007-01'],
    'A014': ['G-CCOS270-01', 'G-CCOS280-01', 'G-ICCS270-01', 'G-ICCS258-02'],
    'A015': ['G-CCOS008-02', 'G-CCOS013-01', 'G-ICCS007-01'],
}


def ya_existe(arbol, xp, **v):
    return bool(arbol.xpath(xp, **v))


def main():
    mat, pro, alu, gru, ins = (cargar(e) for e in ('materias', 'profesores', 'alumnos', 'grupos', 'inscripciones'))

    # ── materias ──
    nombre_mat = {m.get('id'): texto(m, 'nombre') for m in mat.xpath('//materia')}
    for mid, nom, desc, cred, sem, prof, pre in MATERIAS:
        if ya_existe(mat, '//materia[@id=$i]', i=mid):
            continue
        for r in pre:
            if r not in nombre_mat and r not in [x[0] for x in MATERIAS]:
                raise SystemExit(f'Prerrequisito inexistente {r} para {mid}')
        m = sub(mat.getroot(), 'materia', id=mid, clave=f'{mid[:4]} {mid[4:]}')
        sub(m, 'nombre', nom); sub(m, 'descripcion', desc); sub(m, 'creditos', cred); sub(m, 'semestre', sem)
        sub(m, 'carrera', 'Ingeniería en Ciencias de la Computación', codigo='ICC')
        nombre_prof = {'P012': 'Eduardo Profesor', 'P002': 'Carlos Palomino-Jiménez', 'P003': 'Beatriz Beltrán-Martínez',
                       **{p[0]: p[1] for p in PROFESORES}}[prof]
        sub(m, 'profesor', nombre_prof, id=prof)
        pr = sub(m, 'prerrequisitos')
        nombre_mat[mid] = nom
        for r in pre:
            sub(pr, 'prerrequisito', ref=r, nombre=nombre_mat.get(r, r))
        informe['agregado'].append(f'materia {mid} {nom}')
    guardar(mat, 'materias')

    # ── profesores ──
    for pid, nom, esp in PROFESORES:
        if ya_existe(pro, '//profesor[@id=$i]', i=pid):
            continue
        p = sub(pro.getroot(), 'profesor', id=pid)
        sub(p, 'nombre', nom); sub(p, 'especialidad', esp); sub(p, 'correo', f'{slug(nom)}@universidad.edu.mx')
        sub(p, 'departamento', 'Sistemas'); sub(p, 'materias_impartidas')
        informe['agregado'].append(f'profesor {pid} {nom}')

    # ── alumnos (promedio provisional; se recalcula al final) ──
    for aid, matr, nom, ape, carr, sem in ALUMNOS:
        if ya_existe(alu, '//alumno[@id=$i]', i=aid):
            continue
        a = sub(alu.getroot(), 'alumno', id=aid, matricula=matr)
        sub(a, 'nombre', nom); sub(a, 'apellidos', ape); sub(a, 'correo', f'{slug(nom)}.{slug(ape.split()[0])}@alumno.buap.mx')
        sub(a, 'carrera_id', carr); sub(a, 'semestre', sem); sub(a, 'promedio', '0.0'); sub(a, 'estatus', 'Activo')
        informe['agregado'].append(f'alumno {aid} {nom} {ape}')

    # ── grupos ──
    for materia, prof, dias, ini, fin, aula in GRUPOS:
        d = {'materia_id': materia, 'profesor_id': prof, 'periodo': PERIODO, 'dia': dias,
             'hora_inicio': ini, 'hora_fin': fin, 'aula': aula}
        # idempotente: si ya hay un grupo idéntico (misma materia, profe y horario) no se repite
        if gru.xpath('//grupo[materia_id=$m and profesor_id=$p and dia=$d and hora_inicio=$h]', m=materia, p=prof, d=dias, h=ini):
            continue
        problemas = A.problemas_grupo(d, gru, mat, pro)
        if problemas:
            informe['omitido'].append(f'grupo {materia}/{prof} {dias} {ini}: ' + ' '.join(problemas)); continue
        gid = A.siguiente_id_grupo(materia, gru)
        g = sub(gru.getroot(), 'grupo', id=gid)
        for tag in ('materia_id', 'profesor_id', 'periodo', 'dia', 'hora_inicio', 'hora_fin', 'aula'):
            sub(g, tag, d[tag])
        informe['agregado'].append(f'grupo {gid} ({prof}, {dias} {ini}-{fin})')

    # ── inscripciones: historial y periodo actual ──
    def nueva(aid, materia, periodo, cal=None, gid=None):
        i = sub(ins.getroot(), 'inscripcion', id=A.siguiente_id_inscripcion(ins))
        sub(i, 'alumno_id', aid); sub(i, 'materia_id', materia)
        if gid:
            sub(i, 'grupo_id', gid)
        sub(i, 'periodo', periodo)
        if cal is not None:
            sub(i, 'calificacion_final', cal)
            sub(i, 'estatus', 'Aprobado' if cal >= config.CALIFICACION_MINIMA else 'Reprobado')
        else:
            sub(i, 'estatus', 'Cursando')

    for aid, filas in HIST.items():
        for materia, periodo, cal in filas:
            if ins.xpath('//inscripcion[alumno_id=$a and materia_id=$m and periodo=$p]', a=aid, m=materia, p=periodo):
                continue
            faltan = [r for r in A.prerrequisitos_de(materia, mat) if r not in A.aprobadas(aid, ins)]
            if faltan:
                informe['omitido'].append(f'historial {aid} {materia} {periodo}: prerrequisitos sin aprobar {faltan}'); continue
            nueva(aid, materia, periodo, cal)
            informe['agregado'].append(f'historial {aid} {materia} {periodo} = {cal}')
    for aid, grupos in ACTUAL.items():
        for gid in grupos:
            if ins.xpath('//inscripcion[alumno_id=$a and grupo_id=$g]', a=aid, g=gid):
                continue
            problemas = A.problemas_inscripcion(aid, gid, alu, gru, ins, mat)
            if problemas:
                informe['omitido'].append(f'inscripción {aid} -> {gid}: ' + ' '.join(problemas)); continue
            materia = gru.xpath('//grupo[@id=$g]/materia_id/text()', g=gid)[0]
            nueva(aid, materia, PERIODO, None, gid)
            informe['agregado'].append(f'inscripción {aid} -> {gid}')

    # ── promedios (de las calificaciones) y materias_impartidas (de grupos + titular) ──
    for a in alu.xpath('//alumno'):
        notas = [float(n.text) for n in ins.xpath('//inscripcion[alumno_id=$a]/calificacion_final', a=a.get('id')) if n.text]
        if notas:
            a.find('promedio').text = str(round(sum(notas) / len(notas), 1))
    for p in pro.xpath('//profesor'):
        codigos = {m.get('codigo') for m in p.xpath('materias_impartidas/materia')}
        deseadas = set(gru.xpath('//grupo[profesor_id=$p]/materia_id/text()', p=p.get('id')))
        deseadas |= set(mat.xpath('//materia[profesor/@id=$p]/@id', p=p.get('id')))
        cont = p.find('materias_impartidas')
        for c in sorted(deseadas - codigos):
            sub(cont, 'materia', nombre_mat.get(c, c), codigo=c)

    for arbol, ent in ((pro, 'profesores'), (alu, 'alumnos'), (gru, 'grupos'), (ins, 'inscripciones')):
        guardar(arbol, ent)
    if not DRY:
        SemanticEngine.construir_grafo()

    print(('SIMULACIÓN (no se escribió nada)\n' if DRY else '') + f"Agregado: {len(informe['agregado'])} · Omitido: {len(informe['omitido'])}")
    for l in informe['agregado']:
        print('  +', l)
    for l in informe['omitido']:
        print('  ! omitido:', l)


if __name__ == '__main__':
    main()
