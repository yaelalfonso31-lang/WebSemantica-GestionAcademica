import os
from flask import Blueprint, current_app, session
from app.auth.decorators import login_requerido, rol_requerido
from app.services.transformer import transformar_a_html
from lxml import etree

horarios_bp = Blueprint('horarios', __name__)

@horarios_bp.route('/horarios', methods=["GET"])
@login_requerido
@rol_requerido('alumno') #
def vista_horarios():
    xml_inscripciones = os.path.join(current_app.config.get('XML_DIR', 'data/xml'), 'inscripciones.xml')
    xml_grupos = os.path.join(current_app.config.get('XML_DIR', 'data/xml'), 'grupos.xml')
    
    rol_actual = session.get('rol')
    nombre_actual = session.get('username')
    alumno_id_actual = "A001" # ID de prueba simulado

    # 1. Descubrir qué materias está "Cursando" el alumno actualmente
    materias_cursando = []
    if os.path.exists(xml_inscripciones):
        tree_insc = etree.parse(xml_inscripciones)
        # Filtro XPath estricto
        nodos_insc = tree_insc.xpath(f"//inscripcion[alumno_id='{alumno_id_actual}' and estatus='Cursando']")
        for nodo in nodos_insc:
            materia_id = nodo.find('materia_id').text
            materias_cursando.append(materia_id)

    # 2. Construir un XML temporal solo con los grupos de esas materias
    nuevo_root = etree.Element("horario_alumno")
    if os.path.exists(xml_grupos) and materias_cursando:
        tree_grupos = etree.parse(xml_grupos)
        root_grupos = tree_grupos.getroot()
        
        for mat_id in materias_cursando:
            # Extraer grupos que coincidan con la materia
            grupos_materia = root_grupos.xpath(f"//grupo[materia_id='{mat_id}']")
            for g in grupos_materia:
                nuevo_root.append(g)

    xml_data = etree.tostring(nuevo_root, encoding='unicode')

    # 3. Enviar el XML resultante a la vista Bootstrap
    html_generado = transformar_a_html(
        xml_path_or_string=xml_data,
        xslt_filename='horario.xsl',
        params={
            'rol_usuario': rol_actual,
            'nombre_usuario': nombre_actual
        }
    )
    
    return html_generado