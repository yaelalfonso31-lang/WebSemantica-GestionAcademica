import os
from flask import Blueprint, current_app, session
from app.auth.decorators import login_requerido, rol_requerido
from app.services.transformer import transformar_a_html
from lxml import etree

grupos_bp = Blueprint('grupos', __name__)

@grupos_bp.route('/mis_grupos', methods=["GET"])
@login_requerido
@rol_requerido('profesor')
def vista_mis_grupos():
    xml_grupos = os.path.join(current_app.config.get('XML_DIR', 'data/xml'), 'grupos.xml')
    
    rol_actual = session.get('rol')
    nombre_actual = session.get('username')
    # Simulamos el ID del profesor (Eduardo) basándonos en tu usuarios.xml
    profesor_id_actual = "P002" 

    nuevo_root = etree.Element("mis_grupos")

    if os.path.exists(xml_grupos):
        tree_grupos = etree.parse(xml_grupos)
        root_grupos = tree_grupos.getroot()
        
        # Filtramos mediante XPath los grupos asignados a este profesor
        grupos_asignados = root_grupos.xpath(f"//grupo[profesor_id='{profesor_id_actual}']")
        
        for g in grupos_asignados:
            nuevo_root.append(g)

    xml_data = etree.tostring(nuevo_root, encoding='unicode')

    html_generado = transformar_a_html(
        xml_path_or_string=xml_data,
        xslt_filename='mis_grupos.xsl',
        params={
            'rol_usuario': rol_actual,
            'nombre_usuario': nombre_actual
        }
    )
    
    return html_generado