import os
from lxml import etree
from flask import Blueprint, current_app, session, request, jsonify
from app.auth.decorators import login_requerido, rol_requerido
from app.services.transformer import transformar_a_html
from app.services.xml_repository import XMLRepository

alumnos_bp = Blueprint('alumnos', __name__)

# Instanciamos el repositorio apuntando a alumnos.xml
repo = XMLRepository(entidad="alumnos")

@alumnos_bp.route('/alumnos', methods=["GET"])
@login_requerido
@rol_requerido('admin') #
def vista_alumnos():
    """Renderiza la vista de alumnos transformando alumnos.xml con XSLT."""
    
    xml_path = os.path.join(current_app.config.get('XML_DIR', 'data/xml'), 'alumnos.xml')
    rol_actual = session.get('rol', 'visitante')
    nombre_actual = session.get('username', 'Invitado')
    
    if not os.path.exists(xml_path):
        xml_data = '<?xml version="1.0" encoding="UTF-8"?><alumnos></alumnos>'
        return transformar_a_html(xml_data, 'alumnos.xsl', {'rol_usuario': rol_actual, 'nombre_usuario': nombre_actual})
    
    html_generado = transformar_a_html(
        xml_path_or_string=xml_path,
        xslt_filename='alumnos.xsl',
        params={
            'rol_usuario': rol_actual,
            'nombre_usuario': nombre_actual
        }
    )
    
    return html_generado


@alumnos_bp.route("/api/alumnos", methods=["GET"])
@login_requerido
@rol_requerido('admin', 'profesor')
def api_listar_alumnos():
    """Devuelve la lista de alumnos en formato JSON."""
    return jsonify(repo.listar_alumnos()), 200

@alumnos_bp.route("/api/alumnos", methods=["POST"])
@login_requerido
@rol_requerido('admin')
def api_crear_alumno():
    """Recibe datos para crear un nuevo alumno, validando contra DTD y XSD."""
    datos = request.get_json(silent=True) or request.form.to_dict()
    try:
        creado = repo.agregar_alumno(datos)
        return jsonify({"mensaje": "Alumno registrado correctamente", "alumno": creado}), 201
    except KeyError as e:
        return jsonify({"error": f"Falta el campo obligatorio {e}."}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@alumnos_bp.route("/api/alumnos/<alumno_id>", methods=["DELETE"])
@login_requerido
@rol_requerido('admin')
def api_eliminar_alumno(alumno_id):
    """Elimina un alumno por su atributo ID."""
    eliminado = repo.eliminar_alumno(alumno_id)
    if not eliminado:
        return jsonify({"error": "Alumno no encontrado"}), 404
    return jsonify({"mensaje": "Alumno eliminado correctamente"}), 200

@alumnos_bp.route('/api/alumnos/<alumno_id>', methods=["PUT"])
@login_requerido
@rol_requerido('admin')
def api_editar_alumno(alumno_id):
    datos = request.get_json(silent=True) or {}
    xml_path = os.path.join(current_app.config.get('XML_DIR', 'data/xml'), 'alumnos.xml')
    
    if not os.path.exists(xml_path):
        return jsonify({"error": "Archivo XML no encontrado"}), 404
        
    tree = etree.parse(xml_path)
    root = tree.getroot()
    
    # Buscar el alumno por su atributo ID
    nodos = root.xpath("//alumno[@id=$i]", i=alumno_id)
    if not nodos:
        return jsonify({"error": "Alumno no encontrado"}), 404
        
    alumno = nodos[0]
    
    # Actualizar los atributos y nodos hijos
    if 'matricula' in datos:
        alumno.set('matricula', datos['matricula'])
    
    campos = ['nombre', 'apellidos', 'correo', 'carrera_id', 'semestre', 'promedio', 'estatus']
    for campo in campos:
        if campo in datos:
            nodo_campo = alumno.find(campo)
            if nodo_campo is not None:
                nodo_campo.text = str(datos[campo])
            else:
                # Si el nodo no existía, lo creamos
                nuevo_nodo = etree.SubElement(alumno, campo)
                nuevo_nodo.text = str(datos[campo])

    # Guardar cambios y actualizar el grafo semántico
    tree.write(xml_path, encoding="UTF-8", xml_declaration=True, pretty_print=True)
    
    from app.services.rdf_graph import SemanticEngine
    SemanticEngine.construir_grafo()
    
    return jsonify({"mensaje": "Alumno actualizado correctamente"}), 200