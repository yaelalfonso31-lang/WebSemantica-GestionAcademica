from flask import Blueprint, jsonify, request, session

from app.auth.decorators import login_requerido, rol_requerido
from app.services import academic_metrics as metricas
from app.services import asignaciones as asig
from app.services.transformer import transformar_a_html

grupos_bp = Blueprint('grupos', __name__)


@grupos_bp.route('/mis_grupos', methods=['GET'])
@login_requerido
@rol_requerido('profesor')
def vista_mis_grupos():
    """Grupos asignados al profesor que inició sesión."""
    return transformar_a_html(
        xml_path_or_string=metricas.xml_mis_grupos(session.get('ref_id')),
        xslt_filename='mis_grupos.xsl',
        params={'rol_usuario': session.get('rol'),
                'nombre_usuario': session.get('nombre') or session.get('username')},
    )


# ───────────────────── administración de grupos e inscripciones ─────────────────────
@grupos_bp.route('/grupos', methods=['GET'])
@login_requerido
@rol_requerido('admin')
def vista_grupos_admin():
    """Todos los grupos del periodo, con alta de grupos e inscripción de alumnos."""
    return transformar_a_html(
        xml_path_or_string=metricas.xml_admin_grupos(),
        xslt_filename='grupos_admin.xsl',
        params={'rol_usuario': session.get('rol'),
                'nombre_usuario': session.get('nombre') or session.get('username')},
    )


@grupos_bp.route('/api/grupos', methods=['POST'])
@login_requerido
@rol_requerido('admin')
def api_crear_grupo():
    datos = request.get_json(silent=True) or {}
    campos = ('materia_id', 'profesor_id', 'periodo', 'dia', 'hora_inicio', 'hora_fin', 'aula')
    limpio = {c: str(datos.get(c, '')).strip() for c in campos}
    try:
        gid = asig.crear_grupo(limpio)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    return jsonify({'mensaje': f'Grupo {gid} creado correctamente.', 'id': gid}), 201


@grupos_bp.route('/api/grupos/<grupo_id>', methods=['DELETE'])
@login_requerido
@rol_requerido('admin')
def api_eliminar_grupo(grupo_id):
    try:
        asig.eliminar_grupo(grupo_id)
    except ValueError as e:
        return jsonify({'error': str(e)}), 409
    return jsonify({'mensaje': f'Grupo {grupo_id} eliminado.'}), 200


@grupos_bp.route('/api/inscripciones', methods=['POST'])
@login_requerido
@rol_requerido('admin')
def api_inscribir():
    datos = request.get_json(silent=True) or {}
    try:
        iid = asig.inscribir(str(datos.get('alumno_id', '')).strip(), str(datos.get('grupo_id', '')).strip())
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    return jsonify({'mensaje': f'Inscripción {iid} registrada.', 'id': iid}), 201


@grupos_bp.route('/api/inscripciones/<inscripcion_id>', methods=['DELETE'])
@login_requerido
@rol_requerido('admin')
def api_dar_de_baja(inscripcion_id):
    try:
        asig.dar_de_baja(inscripcion_id)
    except ValueError as e:
        return jsonify({'error': str(e)}), 409
    return jsonify({'mensaje': 'Inscripción dada de baja.'}), 200
