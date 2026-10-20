from flask import Blueprint, session

from app.auth.decorators import login_requerido, rol_requerido
from app.services import academic_metrics as metricas
from app.services.transformer import transformar_a_html

horarios_bp = Blueprint('horarios', __name__)


@horarios_bp.route('/horarios', methods=['GET'])
@login_requerido
@rol_requerido('alumno')
def vista_horarios():
    """Grupos de las materias que el alumno cursa actualmente."""
    return transformar_a_html(
        xml_path_or_string=metricas.xml_horario(session.get('ref_id')),
        xslt_filename='horario.xsl',
        params={'rol_usuario': session.get('rol'),
                'nombre_usuario': session.get('nombre') or session.get('username')},
    )
