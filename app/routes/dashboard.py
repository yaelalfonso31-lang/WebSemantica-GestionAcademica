import os
from flask import Blueprint, session, current_app
from app.auth.decorators import login_requerido
from app.services.transformer import transformar_a_html

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
@login_requerido
def vista_dashboard():
    rol_actual = session.get('rol')
    nombre_actual = session.get('username')
    
    # Dependiendo del rol, elegimos qué XSLT usar para pintar el panel
    if rol_actual == 'admin':
        xslt_file = 'dashboard_admin.xsl'
        xml_data = '<dashboard><tipo>administrativo</tipo></dashboard>'
    elif rol_actual == 'profesor':
        xslt_file = 'dashboard_profesor.xsl'
        xml_data = '<dashboard><tipo>docente</tipo></dashboard>'
    elif rol_actual == 'alumno':
        xslt_file = 'dashboard_alumno.xsl'
        xml_data = '<dashboard><tipo>estudiante</tipo></dashboard>'
    else:
        xslt_file = 'dashboard.xsl'
        xml_data = '<dashboard></dashboard>'

    # Transformamos un XML en memoria hacia el XSLT correspondiente
    html_generado = transformar_a_html(
        xml_path_or_string=xml_data,
        xslt_filename=xslt_file,
        params={'rol_usuario': rol_actual, 'nombre_usuario': nombre_actual}
    )
    
    return html_generado