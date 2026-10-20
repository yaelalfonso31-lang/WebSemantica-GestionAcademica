from flask import Blueprint, session

from app.auth.decorators import login_requerido, rol_requerido
from app.services import academic_metrics as metricas
from app.services.transformer import transformar_a_html

kardex_bp = Blueprint('kardex', __name__)


@kardex_bp.route('/kardex', methods=['GET'])
@login_requerido
@rol_requerido('alumno')
def vista_kardex():
    """Historial académico del alumno que inició sesión (nunca el de otro)."""
    return transformar_a_html(
        xml_path_or_string=metricas.xml_kardex(session.get('ref_id')),
        xslt_filename='kardex.xsl',
        params={'rol_usuario': session.get('rol'),
                'nombre_usuario': session.get('nombre') or session.get('username')},
    )
