from flask import Blueprint, jsonify
from app.auth.decorators import login_requerido, rol_requerido
from app.services.sparql_engine import SPARQLEngine

consultas_bp = Blueprint('consultas', __name__)

@consultas_bp.route('/api/consultas/riesgo', methods=["GET"])
@login_requerido
@rol_requerido('admin', 'profesor') # Solo admins y profesores pueden ver esto
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