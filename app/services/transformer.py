import os

from flask import current_app, get_flashed_messages
from lxml import etree
from markupsafe import escape

from app.services.paths import ruta

_CATEGORIAS = {'danger', 'warning', 'success', 'info'}
_MARCA_MAIN = '<main class="layout-main">'


def _html_mensajes_flash():
    """Los flash() de Flask no llegan a XSLT por sí solos: se inyectan al inicio de <main>."""
    try:
        mensajes = get_flashed_messages(with_categories=True)
    except RuntimeError:  # sin contexto de petición
        return ''
    if not mensajes:
        return ''
    alertas = ''.join(
        f'<div class="alert alert-{cat if cat in _CATEGORIAS else "info"} alert-dismissible fade show" role="alert">'
        f'{escape(msg)}<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Cerrar"></button></div>'
        for cat, msg in mensajes
    )
    return f'<div class="container mt-3">{alertas}</div>'


def _error(mensaje, codigo=500):
    return f'<h1>Error {codigo}</h1><p>{escape(mensaje)}</p>', codigo


def transformar_a_html(xml_path_or_string, xslt_filename, params=None):
    # 1. Cargar la hoja de transformación XSLT (ruta absoluta: no depende del cwd)
    xslt_path = ruta('XSLT_DIR', 'html', xslt_filename)
    if not os.path.exists(xslt_path):
        current_app.logger.error('No se encontró el XSLT: %s', xslt_path)
        return _error('No se encontró la plantilla de la vista.')

    try:
        transform = etree.XSLT(etree.parse(xslt_path))

        # 2. XML: ruta a un archivo físico o string generado al vuelo
        if xml_path_or_string.strip().startswith('<'):
            xml_doc = etree.fromstring(xml_path_or_string.encode('utf-8'))
        else:
            xml_doc = etree.parse(xml_path_or_string)

        # 3. Parámetros para el XSLT (strparam evita que un valor se interprete como XPath)
        xslt_params = {k: etree.XSLT.strparam(str(v)) for k, v in (params or {}).items()}

        # 4. Transformar
        html = str(transform(xml_doc, **xslt_params))
    except (etree.XMLSyntaxError, etree.XSLTParseError, etree.XSLTApplyError, OSError) as e:
        current_app.logger.exception('Fallo al transformar %s: %s', xslt_filename, e)
        return _error('No se pudo generar la vista. Revisa el log del servidor.')

    return html.replace(_MARCA_MAIN, _MARCA_MAIN + _html_mensajes_flash(), 1)
