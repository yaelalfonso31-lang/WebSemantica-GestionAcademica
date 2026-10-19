import os
from flask import Blueprint, current_app, session, request, jsonify
from app.auth.decorators import login_requerido, rol_requerido
from app.services.transformer import transformar_a_html
from app.services.rdf_graph import SemanticEngine
from lxml import etree

calificaciones_bp = Blueprint('calificaciones', __name__)

@calificaciones_bp.route('/calificar', methods=["GET"])
@login_requerido
@rol_requerido('profesor')
def vista_calificar():
    # Obtenemos los parámetros de la URL enviados desde el botón "Calificar Alumnos"
    grupo_id = request.args.get('grupo', '')
    materia_id = request.args.get('materia', '')
    
    xml_insc = os.path.join(current_app.config.get('XML_DIR', 'data/xml'), 'inscripciones.xml')
    rol_actual = session.get('rol')
    nombre_actual = session.get('username')
    
    # Creamos un nodo raíz temporal para enviar al XSLT
    nuevo_root = etree.Element("evaluacion", grupo=grupo_id, materia=materia_id)
    
    if os.path.exists(xml_insc) and materia_id:
        tree = etree.parse(xml_insc)
        # Filtramos a los alumnos inscritos en esta materia en particular
        inscripciones = tree.xpath(f"//inscripcion[materia_id='{materia_id}']")
        for insc in inscripciones:
            nuevo_root.append(insc)
            
    xml_data = etree.tostring(nuevo_root, encoding='unicode')
    
    return transformar_a_html(
        xml_path_or_string=xml_data,
        xslt_filename='calificaciones.xsl',
        params={'rol_usuario': rol_actual, 'nombre_usuario': nombre_actual}
    )

@calificaciones_bp.route('/api/calificar', methods=["POST"])
@login_requerido
@rol_requerido('profesor')
def guardar_calificaciones():
    datos = request.json
    xml_insc = os.path.join(current_app.config.get('XML_DIR', 'data/xml'), 'inscripciones.xml')
    
    if not os.path.exists(xml_insc):
        return jsonify({"error": "No se encontró la base de datos de inscripciones."}), 404
        
    tree = etree.parse(xml_insc)
    root = tree.getroot()
    
    # Recorremos el diccionario de datos enviados desde el navegador
    for insc_id, valores in datos.items():
        nodo = root.xpath(f"//inscripcion[@id='{insc_id}']")
        if nodo:
            insc_node = nodo[0]
            
            # Actualizar o crear nodo de calificación
            calif_node = insc_node.find('calificacion_final')
            if calif_node is None:
                calif_node = etree.SubElement(insc_node, 'calificacion_final')
            calif_node.text = str(valores.get('calificacion', ''))
            
            # Actualizar nodo de estatus
            estatus_node = insc_node.find('estatus')
            if estatus_node is None:
                estatus_node = etree.SubElement(insc_node, 'estatus')
            estatus_node.text = str(valores.get('estatus', 'Cursando'))
            
    # Guardamos los cambios físicos en el XML
    tree.write(xml_insc, encoding="UTF-8", xml_declaration=True, pretty_print=True)
    
    # ¡MAGIA SEMÁNTICA! Reconstruimos el grafo para que asimile las nuevas calificaciones
    SemanticEngine.construir_grafo()
    
    return jsonify({"mensaje": "Calificaciones guardadas y Grafo RDF actualizado con éxito."})