from flask import Blueprint, session

from app.auth.decorators import login_requerido, rol_requerido
from app.services import academic_metrics as metricas
from app.services.transformer import transformar_a_html

horarios_bp = Blueprint('horarios', __name__)


@horarios_bp.route('/horarios', methods=['GET'])
@login_requerido
@rol_requerido('alumno', 'profesor')
def vista_horarios():
    """Horario semanal: el alumno ve sus materias en curso y el profesor los grupos que imparte."""
    ref = session.get('ref_id')
    xml = metricas.xml_horario_profesor(ref) if session.get('rol') == 'profesor' else metricas.xml_horario(ref)
    return transformar_a_html(
        xml_path_or_string=xml,
        xslt_filename='horario.xsl',
        params={'rol_usuario': session.get('rol'),
                'nombre_usuario': session.get('nombre') or session.get('username')},
    )
