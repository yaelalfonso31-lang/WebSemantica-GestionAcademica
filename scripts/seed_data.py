"""Genera datos de ejemplo COHERENTES entre sí (usuarios, profesores, grupos, inscripciones).

Uso (desde la raíz):  python scripts/seed_data.py
Es idempotente: se puede correr varias veces. Hace respaldo de lo que sobrescribe en data/backups/.

Qué arregla: los XML usaban IDs que no coincidían (usuario U003 vs alumno A006, grupos con
P001/MAT-101 que no existían, inscripciones con M001...). Aquí todo apunta a IDs reales.
NOTA: especialidad/correo de los profesores nuevos son datos de ejemplo; reemplázalos.
"""
import os
import re
import shutil
import sys
import unicodedata
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from lxml import etree  # noqa: E402

import config  # noqa: E402
from app.services.security import hashear_contrasena  # noqa: E402

PERIODO = config.PERIODO_ACTUAL
PASSWORD_DEMO = '1234'   # solo para desarrollo: cámbiala

# usuario -> (id, username, nombre, rol, ref)
USUARIOS = [
    ('U001', 'admin', 'Administrador General', 'admin', None),
    ('U002', 'profe', 'Eduardo Profesor', 'profesor', 'P012'),
    ('U003', 'alumno', 'Yael Serrano', 'alumno', 'A006'),
]

# (id, materia, profesor, dias, inicio, fin, aula)
GRUPOS = [
    ('G-CCOS005-01', 'CCOS005', 'P001', 'Lunes y Miércoles', '07:00', '09:00', 'Edificio 1 - Aula 101'),
    ('G-CCOS005-02', 'CCOS005', 'P012', 'Martes y Jueves', '07:00', '09:00', 'Edificio 1 - Aula 102'),
    ('G-CCOS008-01', 'CCOS008', 'P002', 'Lunes y Miércoles', '09:00', '11:00', 'Edificio 1 - Aula 104'),
    ('G-CCOS013-01', 'CCOS013', 'P003', 'Martes y Jueves', '09:00', '11:00', 'Laboratorio de Cómputo A'),
    ('G-CCOS252-01', 'CCOS252', 'P004', 'Lunes y Miércoles', '11:00', '13:00', 'Laboratorio de Cómputo B'),
    ('G-ICCS004-01', 'ICCS004', 'P006', 'Martes y Jueves', '11:00', '13:00', 'Edificio 2 - Aula 201'),
    ('G-ICCS006-01', 'ICCS006', 'P007', 'Viernes', '09:00', '12:00', 'Edificio 2 - Aula 202'),
    ('G-ICCS007-01', 'ICCS007', 'P001', 'Lunes y Miércoles', '13:00', '15:00', 'Laboratorio de Electrónica'),
    ('G-ICCS250-01', 'ICCS250', 'P008', 'Martes y Jueves', '13:00', '15:00', 'Laboratorio de Electrónica'),
    ('G-ICCS256-01', 'ICCS256', 'P009', 'Lunes y Miércoles', '15:00', '17:00', 'Laboratorio de Cómputo C'),
    ('G-ICCS256-02', 'ICCS256', 'P012', 'Viernes', '12:00', '15:00', 'Laboratorio de Cómputo C'),
    ('G-ICCS257-01', 'ICCS257', 'P010', 'Martes y Jueves', '15:00', '17:00', 'Laboratorio de Cómputo A'),
    ('G-ICCS258-01', 'ICCS258', 'P011', 'Lunes y Miércoles', '17:00', '19:00', 'Laboratorio de Cómputo B'),
    ('G-ICCS258-02', 'ICCS258', 'P012', 'Martes y Jueves', '17:00', '19:00', 'Laboratorio de Cómputo B'),
]

# Historial: (alumno, materia, periodo, calificacion|None, grupo|None). El estatus se deriva de la nota.
H = {
    'A001': [('CCOS008', 'Primavera 2026', 95.0, None),
             ('CCOS005', PERIODO, None, 'G-CCOS005-02'), ('CCOS013', PERIODO, None, 'G-CCOS013-01'),
             ('ICCS004', PERIODO, None, 'G-ICCS004-01')],
    'A002': [('CCOS005', 'Otoño 2025', 85.0, None), ('CCOS008', 'Otoño 2025', 90.0, None),
             ('CCOS013', 'Primavera 2026', 88.0, None), ('CCOS252', 'Primavera 2026', 84.0, None),
             ('ICCS004', 'Otoño 2025', 92.0, None), ('ICCS007', 'Primavera 2026', 85.0, None),
             ('ICCS250', PERIODO, None, 'G-ICCS250-01'), ('ICCS256', PERIODO, None, 'G-ICCS256-02'),
             ('ICCS258', PERIODO, None, 'G-ICCS258-02')],
    'A003': [('CCOS013', 'Otoño 2025', 95.0, None), ('ICCS004', 'Primavera 2026', 93.5, None),
             ('CCOS252', PERIODO, None, 'G-CCOS252-01'), ('ICCS007', PERIODO, None, 'G-ICCS007-01'),
             ('ICCS258', PERIODO, None, 'G-ICCS258-02')],
    'A005': [('CCOS005', PERIODO, None, 'G-CCOS005-02'), ('CCOS008', PERIODO, None, 'G-CCOS008-01')],
    'A006': [('CCOS005', 'Otoño 2023', 90.0, None), ('CCOS008', 'Otoño 2023', 85.0, None),
             ('CCOS013', 'Primavera 2024', 88.0, None), ('CCOS252', 'Otoño 2024', 92.0, None),
             ('ICCS004', 'Primavera 2024', 80.0, None), ('ICCS006', 'Otoño 2024', 86.0, None),
             ('ICCS007', 'Otoño 2024', 90.0, None), ('ICCS250', 'Primavera 2025', 94.0, None),
             ('ICCS256', 'Primavera 2025', 89.0, None), ('ICCS257', 'Primavera 2026', 55.0, None),
             ('ICCS257', PERIODO, None, 'G-ICCS257-01'), ('ICCS258', PERIODO, None, 'G-ICCS258-02')],
}


def t(padre, tag, texto=None, **attrs):
    e = etree.SubElement(padre, tag, **attrs)
    if texto is not None:
        e.text = str(texto)
    return e


def guardar(raiz, entidad, doctype=None):
    path = os.path.join(config.XML_DIR, f'{entidad}.xml')
    os.makedirs(config.BACKUP_DIR, exist_ok=True)
    if os.path.exists(path):
        shutil.copy2(path, os.path.join(config.BACKUP_DIR, f"{entidad}_{datetime.now():%Y-%m-%d_%H%M%S}.xml"))
    etree.ElementTree(raiz).write(path, encoding='UTF-8', xml_declaration=True, pretty_print=True, doctype=doctype)
    print('escrito', path)


def slug(texto):
    s = unicodedata.normalize('NFKD', texto).encode('ascii', 'ignore').decode()
    return re.sub(r'[^a-z0-9]+', '.', s.lower()).strip('.')


def main():
    parser = etree.XMLParser(remove_blank_text=True)
    materias = {m.get('id'): m for m in etree.parse(os.path.join(config.XML_DIR, 'materias.xml'), parser).xpath('//materia')}
    nombre_mat = {i: m.findtext('nombre').strip() for i, m in materias.items()}
    grupos_ids = {g[0] for g in GRUPOS}

    # ── usuarios (contraseñas hasheadas + vínculo ref) ──
    raiz = etree.Element('usuarios')
    for uid, user, nombre, rol, ref in USUARIOS:
        u = t(raiz, 'usuario', id=uid)
        t(u, 'username', user); t(u, 'password', hashear_contrasena(PASSWORD_DEMO))
        t(u, 'nombre', nombre); t(u, 'rol', rol)
        if ref:
            t(u, 'ref', ref)
    guardar(raiz, 'usuarios')

    # ── grupos ──
    raiz = etree.Element('grupos')
    for gid, mat, prof, dia, ini, fin, aula in GRUPOS:
        g = t(raiz, 'grupo', id=gid)
        t(g, 'materia_id', mat); t(g, 'profesor_id', prof); t(g, 'periodo', PERIODO)
        t(g, 'dia', dia); t(g, 'hora_inicio', ini); t(g, 'hora_fin', fin); t(g, 'aula', aula)
    guardar(raiz, 'grupos')

    # ── profesores: se conservan los existentes y se agregan los que faltan ──
    ruta_prof = os.path.join(config.XML_DIR, 'profesores.xml')
    arbol = etree.parse(ruta_prof, parser)
    raiz = arbol.getroot()
    existentes = {p.get('id') for p in raiz.findall('profesor')}
    nombres = {}
    for m in materias.values():
        p = m.find('profesor')
        nombres[p.get('id')] = p.text.strip()
    nombres['P012'] = 'Eduardo Profesor'
    for pid in sorted(nombres):
        if pid in existentes:
            continue
        impartidas = []
        for gid, mat, prof, *_ in GRUPOS:
            if prof == pid and mat not in impartidas:
                impartidas.append(mat)
        for mid, m in materias.items():            # titular del catálogo aunque no tenga grupo
            if m.find('profesor').get('id') == pid and mid not in impartidas:
                impartidas.append(mid)
        p = t(raiz, 'profesor', id=pid)
        t(p, 'nombre', nombres[pid])
        t(p, 'especialidad', nombre_mat[impartidas[0]] if impartidas else 'Por definir')
        t(p, 'correo', f"{slug(nombres[pid])}@universidad.edu.mx")
        t(p, 'departamento', 'Sistemas')
        mi = t(p, 'materias_impartidas')
        for mid in impartidas:
            t(mi, 'materia', nombre_mat[mid], codigo=mid)
    guardar(raiz, 'profesores', '<!DOCTYPE profesores SYSTEM "../../schemas/dtd/profesores.dtd">')

    # ── inscripciones ──
    raiz = etree.Element('inscripciones')
    n = 0
    for alumno, filas in H.items():
        for mat, periodo, cal, gid in filas:
            n += 1
            if gid is None:
                gid = next((g[0] for g in GRUPOS if g[1] == mat and g[0].endswith('-01')), None)
            assert gid is None or gid in grupos_ids
            i = t(raiz, 'inscripcion', id=f'I{n:03d}')
            t(i, 'alumno_id', alumno); t(i, 'materia_id', mat)
            if gid and periodo == PERIODO:
                t(i, 'grupo_id', gid)
            t(i, 'periodo', periodo)
            if cal is not None:
                t(i, 'calificacion_final', cal)
                t(i, 'estatus', 'Aprobado' if cal >= config.CALIFICACION_MINIMA else 'Reprobado')
            else:
                t(i, 'estatus', 'Cursando')
    guardar(raiz, 'inscripciones', '<!DOCTYPE inscripciones SYSTEM "../../schemas/dtd/inscripciones.dtd">')

    # ── alumnos.promedio recalculado desde las calificaciones ──
    ruta_al = os.path.join(config.XML_DIR, 'alumnos.xml')
    al = etree.parse(ruta_al, parser)
    for aid, filas in H.items():
        notas = [f[2] for f in filas if f[2] is not None]
        nodo = al.xpath('//alumno[@id=$a]', a=aid)
        if notas and nodo:
            nodo[0].find('promedio').text = str(round(sum(notas) / len(notas), 1))
    guardar(al.getroot(), 'alumnos', '<!DOCTYPE alumnos SYSTEM "../../schemas/dtd/alumnos.dtd">')


if __name__ == '__main__':
    main()
