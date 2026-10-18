from flask import Blueprint, jsonify, request
from app.auth.decorators import login_requerido, rol_requerido
from app.services.sparql_engine import SPARQLEngine

consultas_bp = Blueprint('consultas', __name__)

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