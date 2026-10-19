import os
from flask import Blueprint, current_app, session
from lxml import etree
from app.auth.decorators import login_requerido
from app.services.transformer import transformar_a_html
from app.auth.decorators import login_requerido, rol_requerido


kardex_bp = Blueprint('kardex', __name__)

@kardex_bp.route('/kardex', methods=["GET"])
@login_requerido
@rol_requerido('alumno') #
def vista_kardex():
    """Renderiza el historial académico (Kardex) filtrado por alumno."""
    
    # 1. Obtener datos de la sesión
    rol_actual = session.get('rol', 'visitante')
    nombre_actual = session.get('username', 'Invitado')
    
    # IMPORTANTE: Asumimos que guardas el ID del usuario (ej. 'A001') en la sesión durante el login.
    # Si guardas la matrícula, simplemente ajusta la consulta XPath más abajo.
    alumno_id = session.get('user_id', 'A001') # 'A001' como valor de fallback temporal
    
    # 2. Obtener ruta del archivo XML de inscripciones
    xml_path = os.path.join(current_app.config.get('XML_DIR', 'data/xml'), 'inscripciones.xml')
    
    # 3. Filtrar el XML en memoria usando XPath
    if not os.path.exists(xml_path):
        # Si el archivo no existe, pasamos un XML vacío válido
        xml_filtrado = '<?xml version="1.0" encoding="UTF-8"?><inscripciones></inscripciones>'
    else:
        try:
            tree = etree.parse(xml_path)
            root = tree.getroot()
            
            # Creamos un nuevo árbol raíz temporal para el XSLT
            nuevo_root = etree.Element("inscripciones")
            
            # Si es admin o profesor, dejamos que vea todo. Si es alumno, filtramos por su ID.
            if rol_actual in ['admin', 'profesor']:
                nodos_inscripcion = root.xpath('//inscripcion')
            else:
                nodos_inscripcion = root.xpath(f"//inscripcion[alumno_id='{alumno_id}']")
            
            # Agregamos los nodos filtrados al nuevo árbol
            for nodo in nodos_inscripcion:
                nuevo_root.append(nodo)
                
            # Convertimos el árbol recortado a string para pasarlo al transformador
            xml_filtrado = etree.tostring(nuevo_root, encoding='utf-8').decode('utf-8')
            
        except Exception as e:
            print(f"Error al procesar inscripciones.xml: {e}")
            xml_filtrado = '<?xml version="1.0" encoding="UTF-8"?><inscripciones></inscripciones>'

    # 4. Transformar a HTML usando la plantilla XSLT de Bootstrap
    html_generado = transformar_a_html(
        xml_path_or_string=xml_filtrado,
        xslt_filename='kardex.xsl',
        params={
            'rol_usuario': rol_actual,
            'nombre_usuario': nombre_actual
        }
    )
    
    return html_generado