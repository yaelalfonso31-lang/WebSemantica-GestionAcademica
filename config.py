import os

# ── Rutas base (absolutas: la app funciona sin importar desde dónde se lance) ──
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
XML_DIR = os.path.join(BASE_DIR, 'data', 'xml')
RDF_DIR = os.path.join(BASE_DIR, 'data', 'rdf')
BACKUP_DIR = os.path.join(BASE_DIR, 'data', 'backups')
XSLT_DIR = os.path.join(BASE_DIR, 'xslt')
SCHEMAS_DIR = os.path.join(BASE_DIR, 'schemas')
SPARQL_DIR = os.path.join(BASE_DIR, 'sparql')
ONTOLOGY_DIR = os.path.join(BASE_DIR, 'ontology')

# ── Seguridad ──
# En producción define la variable de entorno SECRET_KEY. El valor por defecto
# solo existe para desarrollo local.
SECRET_KEY = os.environ.get('SECRET_KEY', 'super_secreto_para_desarrollo')
SECRET_KEY_ES_DE_DESARROLLO = 'SECRET_KEY' not in os.environ
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_SECURE = os.environ.get('SESSION_COOKIE_SECURE') == '1'  # activar tras HTTPS
PERMANENT_SESSION_LIFETIME = 60 * 60 * 8  # 8 horas

# ── Reglas de negocio ──
CALIFICACION_MINIMA = 70   # >= aprueba
ESCALA_MAX = 100
UMBRAL_RIESGO = 80         # promedio < 80 => alumno en riesgo (igual que alumnos_en_riesgo.rq)
PERIODO_ACTUAL = 'Otoño 2026'
