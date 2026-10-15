from flask import Blueprint, session
from app.services.transformer import transformar_a_html

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
# Aquí iría tu @login_requerido importado de decorators.py
def panel_control():
    rol_actual = session.get('rol', 'visitante')
    nombre_actual = session.get('username', 'Invitado')
    
    # 1. Crear un XML dinámico ligero para alimentar el dashboard
    xml_data = f"""
    <dashboard>
        <metricas>
            <metrica nombre="Estado del Sistema">Activo</metrica>
            <metrica nombre="Semestre Actual">2026B</metrica>
        </metricas>
    </dashboard>
    """
    
    # 2. Pasar el XML, el XSLT y los parámetros de sesión al transformador
    html_generado = transformar_a_html(
        xml_path_or_string=xml_data,
        xslt_filename='dashboard.xsl',
        params={
            'rol_usuario': rol_actual,
            'nombre_usuario': nombre_actual
        }
    )
    
    # 3. Devolver la respuesta directamente al navegador (sin usar plantillas Jinja)
    return html_generado