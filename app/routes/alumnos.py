import os
from flask import Blueprint, current_app, session, request, jsonify
from app.auth.decorators import login_requerido
from app.services.transformer import transformar_a_html
from app.services.xml_repository import XMLRepository

alumnos_bp = Blueprint('alumnos', __name__)
# Instanciamos el repositorio apuntando a alumnos.xml
repo = XMLRepository(entidad="alumnos")

# ==========================================
# 1. RUTA DE VISTA WEB (HTML vía XSLT)
# ==========================================
@alumnos_bp.route('/alumnos', methods=["GET"])
@login_requerido
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

# ==========================================
# 2. RUTAS API (CRUD JSON)
# ==========================================
@alumnos_bp.route("/api/alumnos", methods=["GET"])
@login_requerido
def api_listar_alumnos():
    """Devuelve la lista de alumnos en formato JSON."""
    return jsonify(repo.listar_alumnos()), 200

@alumnos_bp.route("/api/alumnos", methods=["POST"])
@login_requerido
def api_crear_alumno():
    """Recibe datos para crear un nuevo alumno, validando contra DTD y XSD."""
    datos = request.get_json() or request.form.to_dict()
    try:
        creado = repo.agregar_alumno(datos)
        return jsonify({"mensaje": "Alumno registrado correctamente", "alumno": creado}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@alumnos_bp.route("/api/alumnos/<alumno_id>", methods=["DELETE"])
@login_requerido
def api_eliminar_alumno(alumno_id):
    """Elimina un alumno por su atributo ID."""
    eliminado = repo.eliminar_alumno(alumno_id)
    if not eliminado:
        return jsonify({"error": "Alumno no encontrado"}), 404
    return jsonify({"mensaje": "Alumno eliminado correctamente"}), 200