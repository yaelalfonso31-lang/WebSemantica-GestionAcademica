from flask import Blueprint, session

from app.auth.decorators import login_requerido
from app.services import academic_metrics as metricas
from app.services.transformer import transformar_a_html

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/dashboard')
@login_requerido
def vista_dashboard():
    rol = session.get('rol')
    ref_id = session.get('ref_id')

    # Según el rol: qué plantilla XSLT usar y qué métricas calcular para ese usuario
    if rol == 'admin':
        xslt_file, xml_data = 'dashboard_admin.xsl', metricas.xml_dashboard_admin()
    elif rol == 'profesor':
        xslt_file, xml_data = 'dashboard_profesor.xsl', metricas.xml_dashboard_profesor(ref_id)
    elif rol == 'alumno':
        xslt_file, xml_data = 'dashboard_alumno.xsl', metricas.xml_dashboard_alumno(ref_id)
    else:
        xslt_file, xml_data = 'dashboard.xsl', '<dashboard></dashboard>'

    return transformar_a_html(
        xml_path_or_string=xml_data,
        xslt_filename=xslt_file,
        params={'rol_usuario': rol, 'nombre_usuario': session.get('nombre') or session.get('username')},
    )
