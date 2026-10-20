"""Utilidades para leer los XML del catálogo."""
import os

from lxml import etree

from app.services.paths import ruta


def ruta_xml(entidad):
    return ruta('XML_DIR', f'{entidad}.xml')


def cargar(entidad):
    """Parsea data/xml/<entidad>.xml. Devuelve None si no existe o está vacío."""
    path = ruta_xml(entidad)
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        return None
    return etree.parse(path, etree.XMLParser(remove_blank_text=True))


def xpath(arbol, expresion, **variables):
    """XPath con variables ($var) en lugar de f-strings: evita inyección XPath."""
    if arbol is None:
        return []
    return arbol.xpath(expresion, **variables)


def texto(nodo, hijo, defecto=''):
    valor = nodo.findtext(hijo)
    return valor.strip() if valor else defecto
