import os
from lxml import etree
from rdflib import Graph
from flask import current_app

class SemanticEngine:
    _grafo_memoria = None

    @classmethod
    def transformar_xml_a_rdf(cls, xml_filename, xslt_filename, output_rdf_filename):
        """Transforma un archivo XML en RDF/XML usando XSLT y lxml."""
        xml_dir = current_app.config.get('XML_DIR', 'data/xml') if current_app else 'data/xml'
        rdf_dir = current_app.config.get('RDF_DIR', 'data/rdf') if current_app else 'data/rdf'

        xml_path = os.path.join(xml_dir, xml_filename)
        xslt_path = os.path.join('xslt', 'rdf', xslt_filename)
        
        if not os.path.exists(xml_path) or not os.path.exists(xslt_path):
            print(f"Advertencia: No se encontró {xml_path} o {xslt_path} para la transformación.")
            return None
            
        # Parsear e instanciar la transformación
        xml_doc = etree.parse(xml_path)
        xslt_doc = etree.parse(xslt_path)
        transform = etree.XSLT(xslt_doc)
        
        # Ejecutar transformación
        rdf_result = transform(xml_doc)
        
        # Guardar el archivo .rdf resultante
        os.makedirs(rdf_dir, exist_ok=True)
        output_path = os.path.join(rdf_dir, output_rdf_filename)
        rdf_result.write(output_path, encoding='utf-8', pretty_print=True)
        return output_path

    @classmethod
    def construir_grafo(cls):
        """Construye el grafo RDF uniendo la ontología y los datos transformados."""
        g = Graph()
        rdf_dir = current_app.config.get('RDF_DIR', 'data/rdf') if current_app else 'data/rdf'
        
        # 1. Cargar las Ontologías base (clases, propiedades y reglas)
        onto_path = os.path.join('ontology', 'academico.ttl')
        reglas_path = os.path.join('ontology', 'reglas.ttl')
        
        if os.path.exists(onto_path) and os.path.getsize(onto_path) > 0:
            g.parse(onto_path, format='turtle')
        if os.path.exists(reglas_path) and os.path.getsize(reglas_path) > 0:
            g.parse(reglas_path, format='turtle')

        # 2. Generar el RDF de Alumnos y Materias
        alumnos_rdf = cls.transformar_xml_a_rdf('alumnos.xml', 'alumnos2rdf.xsl', 'alumnos.rdf')
        materias_rdf = cls.transformar_xml_a_rdf('materias.xml', 'materias2rdf.xsl', 'materias.rdf')
        
        # 3. Inyectar los datos RDF generados al grafo maestro
        if alumnos_rdf and os.path.exists(alumnos_rdf):
            g.parse(alumnos_rdf, format='xml')
        if materias_rdf and os.path.exists(materias_rdf):
            g.parse(materias_rdf, format='xml')

        # 4. Serializar el grafo completo
        os.makedirs(rdf_dir, exist_ok=True)
        grafo_completo_path = os.path.join(rdf_dir, 'grafo_completo.ttl')
        g.serialize(destination=grafo_completo_path, format='turtle')
        
        print(f"Grafo RDF reconstruido exitosamente. Contiene {len(g)} tripletas.")
        cls._grafo_memoria = g
        return g

    @classmethod
    def obtener_grafo(cls):
        """Devuelve el grafo actual en memoria."""
        if cls._grafo_memoria is None:
            return cls.construir_grafo()
        return cls._grafo_memoria

def cargar_grafo():
    return SemanticEngine.construir_grafo()