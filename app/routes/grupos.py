from flask import Blueprint, session

from app.auth.decorators import login_requerido, rol_requerido
from app.services import academic_metrics as metricas
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
