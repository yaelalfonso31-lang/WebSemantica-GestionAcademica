import os
from lxml import etree

class XMLValidator:
    @staticmethod
    def validar_contra_xsd(xml_tree, xsd_path):
        """Valida un árbol XML contra un archivo XSD."""
        if not os.path.exists(xsd_path):
            raise FileNotFoundError(f"No se encontró el esquema XSD: {xsd_path}")
        
        xsd_doc = etree.parse(xsd_path)
        esquema_xsd = etree.XMLSchema(xsd_doc)
        
        if not esquema_xsd.validate(xml_tree):
            # Extraer y formatear los errores para que sean legibles
            errores = [error.message for error in esquema_xsd.error_log]
            raise ValueError(f"Error de validación XSD:\n" + "\n".join(errores))
        return True

    @staticmethod
    def validar_contra_dtd(xml_tree, dtd_path):
        """Valida un árbol XML contra un archivo DTD."""
        if not os.path.exists(dtd_path):
            raise FileNotFoundError(f"No se encontró el esquema DTD: {dtd_path}")
        
        dtd_doc = etree.DTD(dtd_path)
        
        if not dtd_doc.validate(xml_tree):
            errores = [error.message for error in dtd_doc.error_log]
            raise ValueError(f"Error de validación DTD:\n" + "\n".join(errores))
        return True