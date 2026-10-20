import os
from flask import Blueprint, session, request, jsonify
from app.auth.decorators import login_requerido, rol_requerido
from app.services.transformer import transformar_a_html
from app.services.sparql_engine import SPARQLEngine

consultas_bp = Blueprint('consultas', __name__)

@consultas_bp.route('/consultas', methods=["GET"])
@login_requerido
@rol_requerido('admin')
def vista_consultas():
    """Renderiza la interfaz visual del buscador SPARQL."""
    rol_actual = session.get('rol')
    nombre_actual = session.get('username')
    
    # Enviamos un XML vacío solo para que el XSLT tenga una raíz donde anclarse
    xml_data = '<buscador_semantico></buscador_semantico>'
    
    html_generado = transformar_a_html(
        xml_path_or_string=xml_data,
        xslt_filename='consultas.xsl',
        params={'rol_usuario': rol_actual, 'nombre_usuario': nombre_actual}
    )
    return html_generado

@consultas_bp.route('/api/consultas/ejecutar', methods=["POST"])
@login_requerido
@rol_requerido('admin')
def api_ejecutar_consulta():
    """Recibe el nombre del archivo .rq, lo ejecuta en rdflib y devuelve JSON."""
    datos = request.get_json(silent=True) or {}
    archivo_rq = datos.get('archivo')

    if not archivo_rq:
        return jsonify({"error": "No se especificó ningún archivo de consulta."}), 400

    try:
        # El motor SPARQL lee el archivo y consulta el grafo en memoria
        resultados = SPARQLEngine.ejecutar_consulta(archivo_rq)
        return jsonify({
            "mensaje": "Consulta ejecutada correctamente",
            "total_resultados": len(resultados),
            "data": resultados
        }), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except FileNotFoundError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@consultas_bp.route('/api/consultas/riesgo', methods=["GET"])
@login_requerido
@rol_requerido('admin', 'profesor')
def api_alumnos_riesgo():
    """Ejecuta la consulta SPARQL de alumnos en riesgo y devuelve JSON."""
    try:
        resultados = SPARQLEngine.ejecutar_consulta('alumnos_en_riesgo.rq')
        return jsonify({
            "mensaje": "Consulta SPARQL ejecutada con éxito",
            "total_resultados": len(resultados),
            "data": resultados
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@consultas_bp.route('/api/consultas/prerrequisitos', methods=["GET"])
@login_requerido
def api_prerrequisitos_de_materia():
    """Ejecuta sparql/prerrequisitos_de_materia.rq sobre el grafo RDF."""
    try:
        materia_id = request.args.get('materia_id', '').strip().upper()
        resultados = SPARQLEngine.ejecutar_consulta('prerrequisitos_de_materia.rq')
        if materia_id:
            resultados = [r for r in resultados if r.get('materiaId') == materia_id]
        return jsonify({
            "mensaje": "Consulta prerrequisitos_de_materia.rq ejecutada con éxito",
            "total_resultados": len(resultados),
            "data": resultados
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@consultas_bp.route('/api/consultas/materias-disponibles', methods=["GET"])
@login_requerido
def api_materias_disponibles():
    """Ejecuta sparql/materias_disponibles.rq sobre el grafo RDF."""
    try:
        alumno_id = request.args.get('alumno_id', '').strip().upper()
        resultados = SPARQLEngine.ejecutar_consulta('materias_disponibles.rq')
        if alumno_id:
            resultados = [r for r in resultados if r.get('alumnoId') == alumno_id]
        return jsonify({
            "mensaje": "Consulta materias_disponibles.rq ejecutada con éxito",
            "total_resultados": len(resultados),
            "data": resultados
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500