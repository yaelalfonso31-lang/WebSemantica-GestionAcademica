import os
from lxml import etree

def transformar_a_html(xml_path_or_string, xslt_filename, params=None):
    # 1. Cargar la hoja de transformación XSLT
    xslt_path = os.path.join('xslt', 'html', xslt_filename)
    if not os.path.exists(xslt_path):
        return f"<h1>Error</h1><p>No se encontró el archivo XSLT: {xslt_path}</p>"
        
    xslt_doc = etree.parse(xslt_path)
    transform = etree.XSLT(xslt_doc)
    
    # 2. Cargar el XML (puede ser la ruta a un archivo físico o un string XML generado al vuelo)
    try:
        if xml_path_or_string.strip().startswith('<'):
            xml_doc = etree.fromstring(xml_path_or_string.encode('utf-8'))
        else:
            xml_doc = etree.parse(xml_path_or_string)
    except Exception as e:
        return f"<h1>Error parseando XML</h1><p>{str(e)}</p>"
    
    # 3. Preparar los parámetros para inyectarlos al XSLT (ej. el rol del usuario)
    xslt_params = {}
    if params:
        for k, v in params.items():
            # lxml requiere XSLT.strparam para pasar cadenas de texto correctamente
            xslt_params[k] = etree.XSLT.strparam(str(v))
            
    # 4. Ejecutar la transformación
    resultado = transform(xml_doc, **xslt_params)
    return str(resultado)