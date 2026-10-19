import os
from lxml import etree
from flask import Blueprint, current_app, session, request, jsonify
from app.auth.decorators import login_requerido, rol_requerido
from app.services.rdf_graph import SemanticEngine
from app.services.transformer import transformar_a_html
from app.services.xml_repository import XMLRepository
from app.services.sparql_engine import SPARQLEngine

materias_bp = Blueprint('materias', __name__)
# Instanciamos el repositorio apuntando a materias.xml
repo = XMLRepository(entidad="materias")

# ==========================================
# 1. RUTA DE VISTA WEB (HTML vía XSLT)
# ==========================================
@materias_bp.route('/materias', methods=["GET"])
@login_requerido
def vista_materias():
    """Renderiza la vista de materias transformando materias.xml con XSLT."""
    xml_path = os.path.join(current_app.config.get('XML_DIR', 'data/xml'), 'materias.xml')
    rol_actual = session.get('rol', 'visitante')
    nombre_actual = session.get('username', 'Invitado')

    if not os.path.exists(xml_path):
        xml_data = '<?xml version="1.0" encoding="UTF-8"?><materias></materias>'
        return transformar_a_html(
            xml_data,
            'materias.xsl',
            {'rol_usuario': rol_actual, 'nombre_usuario': nombre_actual}
        )

    html_generado = transformar_a_html(
        xml_path_or_string=xml_path,
        xslt_filename='materias.xsl',
        params={
            'rol_usuario': rol_actual,
            'nombre_usuario': nombre_actual
        }
    )

    return html_generado


# ==========================================
# 2. RUTAS API (CRUD JSON)
# ==========================================
@materias_bp.route("/api/materias", methods=["GET"])
@login_requerido
def api_listar_materias():
    """Devuelve la lista de materias en formato JSON."""
    return jsonify(repo.listar_materias()), 200


@materias_bp.route("/api/materias", methods=["POST"])
@login_requerido
def api_crear_materia():
    """Recibe datos para crear una nueva materia, validando contra DTD y XSD."""
    datos = request.get_json() or request.form.to_dict()
    try:
        creada = repo.agregar_materia(datos)
        return jsonify({"mensaje": "Materia registrada correctamente", "materia": creada}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@materias_bp.route("/api/materias/<materia_id>", methods=["DELETE"])
@login_requerido
def api_eliminar_materia(materia_id):
    """Elimina una materia por su atributo ID."""
    try:
        eliminado = repo.eliminar_materia(materia_id)
        if not eliminado:
            return jsonify({"error": "Materia no encontrada"}), 404
        return jsonify({"mensaje": "Materia eliminada correctamente"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@materias_bp.route('/api/materias/<materia_id>', methods=["PUT"])
@login_requerido
@rol_requerido('admin')
def api_editar_materia(materia_id):
    datos = request.json
    xml_path = os.path.join(current_app.config.get('XML_DIR', 'data/xml'), 'materias.xml')
    
    if not os.path.exists(xml_path):
        return jsonify({"error": "Archivo de materias no encontrado"}), 404
        
    tree = etree.parse(xml_path)
    root = tree.getroot()
    
    # Buscar la materia por su ID
    nodos = root.xpath(f"//materia[@id='{materia_id}']")
    if not nodos:
        return jsonify({"error": "Materia no encontrada"}), 404
        
    materia = nodos[0]
    
    # Actualizar los campos clave de la materia
    campos = ['nombre', 'creditos', 'prerrequisito']
    for campo in campos:
        if campo in datos:
            nodo_campo = materia.find(campo)
            if nodo_campo is not None:
                # Si el dato viene vacío y es prerrequisito, podríamos querer borrar el texto
                nodo_campo.text = str(datos[campo]) if datos[campo] else ""
            else:
                # Crear el nodo si no existía previamente
                if datos[campo]:
                    nuevo_nodo = etree.SubElement(materia, campo)
                    nuevo_nodo.text = str(datos[campo])

    # Guardar en el archivo físico y actualizar el motor semántico
    tree.write(xml_path, encoding="UTF-8", xml_declaration=True, pretty_print=True)
    SemanticEngine.construir_grafo()
    
    return jsonify({"mensaje": "Materia actualizada correctamente"}), 200


# ==========================================
# 3. RUTAS DE CONSULTAS SEMÁNTICAS (SPARQL)
# ==========================================
@materias_bp.route("/api/materias/prerrequisitos", methods=["GET"])
@login_requerido
def api_prerrequisitos_materia():
    """Ejecuta sparql/prerrequisitos_de_materia.rq (ruta transitiva tienePrerrequisito+)."""
    try:
        materia_id = request.args.get("materia_id", "").strip().upper()
        resultados = SPARQLEngine.ejecutar_consulta("prerrequisitos_de_materia.rq")
        if materia_id:
            resultados = [r for r in resultados if r.get("materiaId") == materia_id]
        return jsonify({
            "mensaje": "Inferencia de prerrequisitos (tienePrerrequisito+) ejecutada",
            "total_resultados": len(resultados),
            "data": resultados
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@materias_bp.route("/api/materias/disponibles", methods=["GET"])
@login_requerido
def api_materias_disponibles():
    """Ejecuta sparql/materias_disponibles.rq filtrando opcionalmente por alumno_id."""
    try:
        alumno_id = request.args.get("alumno_id", "").strip().upper()
        resultados = SPARQLEngine.ejecutar_consulta("materias_disponibles.rq")
        if alumno_id:
            resultados = [r for r in resultados if r.get("alumnoId") == alumno_id]
        return jsonify({
            "mensaje": "Consulta de materias disponibles ejecutada",
            "total_resultados": len(resultados),
            "data": resultados
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500