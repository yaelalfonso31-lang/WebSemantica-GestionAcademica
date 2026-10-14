from flask import Blueprint, request, jsonify, render_template
from lxml import etree
from app.services.xml_repository import XMLRepository

alumnos_bp = Blueprint("alumnos", __name__)
repo = XMLRepository()

@alumnos_bp.route("/alumnos", methods=["GET"])
def vista_alumnos():
    """Renderiza la vista de alumnos transformando alumnos.xml con XSLT."""
    xml_tree = etree.parse("data/xml/alumnos.xml")
    xsl_tree = etree.parse("xslt/html/alumnos.xsl")
    transform = etree.XSLT(xsl_tree)
    tabla_html = str(transform(xml_tree))
    return render_template("dashboard_alumno.html", tabla_alumnos=tabla_html)

@alumnos_bp.route("/api/alumnos", methods=["GET"])
def api_listar_alumnos():
    """Endpoint JSON equivalente al GET de server.js en Sistema-Semantico-Academico."""
    return jsonify(repo.listar_alumnos()), 200

@alumnos_bp.route("/api/alumnos/<alumno_id>", methods=["GET"])
def api_obtener_alumno(alumno_id):
    alumno = repo.obtener_alumno(alumno_id)
    if not alumno:
        return jsonify({"error": "Alumno no encontrado"}), 404
    return jsonify(alumno), 200

@alumnos_bp.route("/api/alumnos", methods=["POST"])
def api_crear_alumno():
    """Endpoint JSON equivalente al POST de server.js."""
    datos = request.get_json() or request.form.to_dict()
    try:
        creado = repo.agregar_alumno(datos)
        return jsonify({"mensaje": "Alumno registrado correctamente", "alumno": creado}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@alumnos_bp.route("/api/alumnos/<alumno_id>", methods=["PUT"])
def api_actualizar_alumno(alumno_id):
    datos = request.get_json() or request.form.to_dict()
    try:
        actualizado = repo.actualizar_alumno(alumno_id, datos)
        return jsonify({"mensaje": "Alumno actualizado correctamente", "alumno": actualizado}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404

@alumnos_bp.route("/api/alumnos/<alumno_id>", methods=["DELETE"])
def api_eliminar_alumno(alumno_id):
    eliminado = repo.eliminar_alumno(alumno_id)
    if not eliminado:
        return jsonify({"error": "Alumno no encontrado"}), 404
    return jsonify({"mensaje": "Alumno eliminado correctamente"}), 200