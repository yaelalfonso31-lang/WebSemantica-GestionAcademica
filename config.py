import os

# Rutas base
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
XML_DIR = os.path.join(BASE_DIR, 'data', 'xml')
RDF_DIR = os.path.join(BASE_DIR, 'data', 'rdf')
XSLT_DIR = os.path.join(BASE_DIR, 'xslt')

# Seguridad
SECRET_KEY = 'super_secreto_para_desarrollo'

# Reglas de Negocio
CALIFICACION_MINIMA = 70
ESCALA_MAX = 100