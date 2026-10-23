import os
from flask import (Blueprint, current_app, session, request, jsonify)
from lxml import etree
from app.services import asignaciones as asig
from app.auth.decorators import login_requerido, rol_requerido
from app.services.transformer import transformar_a_html
from app.services.xml_repository import XMLRepository
profesores_bp = Blueprint("profesores", __name__)

repo = XMLRepository(entidad="profesores")

# ==========================================
# 1. VISTA WEB
# ==========================================

@profesores_bp.route("/profesores", methods=["GET"])
@login_requerido
@rol_requerido('admin')
def vista_profesores():
    """Renderiza la vista de profesores mediante XSLT."""

    xml_path = os.path.join(current_app.config.get('XML_DIR', 'data/xml'), 'profesores.xml')
    rol_actual = session.get('rol', 'visitante')
    nombre_actual = session.get('username', 'Invitado')

    if not os.path.exists(xml_path):
        return jsonify({
            "error": "No se encontró profesores.xml"
        }), 500

    return transformar_a_html(
        xml_path_or_string=xml_path,
        xslt_filename="profesores.xsl",
        params={
            "rol_usuario": rol_actual,
            "nombre_usuario": nombre_actual
        }
    )


# ==========================================
# 2. API: LISTAR PROFESORES
# ==========================================

@profesores_bp.route("/api/profesores", methods=["GET"])
@login_requerido
def api_listar_profesores():
    return jsonify(repo.listar_profesores()), 200


# ==========================================
# 3. API: CONSULTAR UN PROFESOR
# ==========================================

@profesores_bp.route(
    "/api/profesores/<profesor_id>",
    methods=["GET"]
)
@login_requerido
def api_obtener_profesor(profesor_id):
    profesor = repo.obtener_profesor(profesor_id)

    if profesor is None:
        return jsonify({
            "error": "Profesor no encontrado"
        }), 404

    return jsonify(profesor), 200


# ==========================================
# 4. API: REGISTRAR PROFESOR
# ==========================================

@profesores_bp.route("/api/profesores", methods=["POST"])
@login_requerido
@rol_requerido('admin')
def api_crear_profesor():
    datos = request.get_json(silent=True)

    if datos is None:
        datos = request.form.to_dict()

    if not isinstance(datos, dict):
        return jsonify({
            "error": "Los datos deben enviarse en formato JSON"
        }), 400

    try:
        creado = repo.agregar_profesor(datos)

        return jsonify({
            "mensaje": "Profesor registrado correctamente",
            "profesor": creado
        }), 201

    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    except (etree.DocumentInvalid, etree.XMLSyntaxError) as e:
        return jsonify({
            "error": "El profesor no cumple con el DTD o XSD",
            "detalle": str(e)
        }), 400


# ==========================================
# 5. API: ACTUALIZAR PROFESOR
# ==========================================

@profesores_bp.route(
    "/api/profesores/<profesor_id>",
    methods=["PUT"]
)
@login_requerido
@rol_requerido('admin')
def api_actualizar_profesor(profesor_id):
    datos = request.get_json(silent=True)

    if not isinstance(datos, dict) or not datos:
        return jsonify({
            "error": "Envía un objeto JSON con los datos a actualizar"
        }), 400

    try:
        actualizado = repo.actualizar_profesor(
            profesor_id,
            datos
        )

        if actualizado is None:
            return jsonify({
                "error": "Profesor no encontrado"
            }), 404

        return jsonify({
            "mensaje": "Profesor actualizado correctamente",
            "profesor": actualizado
        }), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    except (etree.DocumentInvalid, etree.XMLSyntaxError) as e:
        return jsonify({
            "error": "Los datos no cumplen con el DTD o XSD",
            "detalle": str(e)
        }), 400


# ==========================================
# 6. API: ELIMINAR PROFESOR
# ==========================================

@profesores_bp.route(
    "/api/profesores/<profesor_id>",
    methods=["DELETE"]
)
@login_requerido
@rol_requerido('admin')
def api_eliminar_profesor(profesor_id):
    problemas = asig.problemas_eliminar_profesor(profesor_id)
    if problemas:
        return jsonify({
            "error": "No se puede eliminar el profesor. " + " ".join(problemas)
        }), 409
    eliminado = repo.eliminar_profesor(profesor_id)

    if not eliminado:
        return jsonify({
            "error": "Profesor no encontrado"
        }), 404

    return jsonify({
        "mensaje": "Profesor eliminado correctamente"
    }), 200
