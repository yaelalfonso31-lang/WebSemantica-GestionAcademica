import os

from lxml import etree
from rdflib import Graph
from flask import current_app


class SemanticEngine:
    _grafo_memoria = None

    @classmethod
    def _get_config_dir(cls, key, default):
        try:
            return current_app.config.get(key, default)
        except RuntimeError:
            return default

    @classmethod
    def transformar_xml_a_rdf(
        cls, xml_filename, xslt_filename, output_rdf_filename
    ):
        """Transforma un XML a RDF/XML mediante XSLT."""

        xml_dir = cls._get_config_dir("XML_DIR", "data/xml")
        rdf_dir = cls._get_config_dir("RDF_DIR", "data/rdf")

        xml_path = os.path.join(xml_dir, xml_filename)
        xslt_path = os.path.join("xslt", "rdf", xslt_filename)
        output_path = os.path.join(rdf_dir, output_rdf_filename)

        if not os.path.exists(xml_path):
            print(f"Advertencia: No se encontró el XML: {xml_path}")
            return None

        if not os.path.exists(xslt_path):
            print(f"Advertencia: No se encontró el XSLT: {xslt_path}")
            return None

        try:
            xml_doc = etree.parse(xml_path)
            xslt_doc = etree.parse(xslt_path)
            transform = etree.XSLT(xslt_doc)
            rdf_result = transform(xml_doc)

            os.makedirs(rdf_dir, exist_ok=True)

            rdf_result.write(
                output_path,
                encoding="UTF-8",
                xml_declaration=True,
                pretty_print=True,
            )

            print(f"RDF generado correctamente: {output_path}")
            return output_path

        except (
            etree.XMLSyntaxError,
            etree.XSLTParseError,
            etree.XSLTApplyError,
            OSError,
        ) as error:
            print(
                f"Error al transformar {xml_filename} "
                f"con {xslt_filename}: {error}"
            )
            return None

    @classmethod
    def construir_grafo(cls):
        """Une la ontología, las reglas y los datos RDF académicos."""

        g = Graph()
        rdf_dir = cls._get_config_dir("RDF_DIR", "data/rdf")

        # 1. Cargar la ontología y las reglas semánticas.
        onto_path = os.path.join("ontology", "academico.ttl")
        reglas_path = os.path.join("ontology", "reglas.ttl")

        for path in (onto_path, reglas_path):
            if os.path.exists(path) and os.path.getsize(path) > 0:
                try:
                    g.parse(path, format="turtle")
                    print(f"Archivo semántico cargado: {path}")
                except Exception as error:
                    print(f"Error al cargar {path}: {error}")
                    raise
            else:
                print(f"Advertencia: Archivo ausente o vacío: {path}")

        # 2. Transformar alumnos, materias y profesores.
        transformaciones = [
            ("alumnos.xml", "alumnos2rdf.xsl", "alumnos.rdf"),
            ("materias.xml", "materias2rdf.xsl", "materias.rdf"),
            ("profesores.xml", "profesores2rdf.xsl", "profesores.rdf"),
        ]

        inscripciones_rdf = cls.transformar_xml_a_rdf('inscripciones.xml', 'inscripciones2rdf.xsl', 'inscripciones.rdf')
        if inscripciones_rdf and os.path.exists(inscripciones_rdf):
            g.parse(inscripciones_rdf, format='xml')

        # 3. Incorporar los RDF generados al grafo maestro.
        for xml_filename, xslt_filename, rdf_filename in transformaciones:
            rdf_path = cls.transformar_xml_a_rdf(
                xml_filename,
                xslt_filename,
                rdf_filename,
            )

            if rdf_path and os.path.exists(rdf_path):
                try:
                    g.parse(rdf_path, format="xml")
                    print(f"RDF incorporado al grafo: {rdf_filename}")
                except Exception as error:
                    print(
                        f"Error al cargar {rdf_filename} "
                        f"en el grafo: {error}"
                    )
                    raise

        # 4. Guardar el grafo completo.
        os.makedirs(rdf_dir, exist_ok=True)
        grafo_completo_path = os.path.join(
            rdf_dir, "grafo_completo.ttl"
        )

        g.serialize(
            destination=grafo_completo_path,
            format="turtle",
        )

        print(
            "Grafo RDF reconstruido exitosamente. "
            f"Contiene {len(g)} tripletas."
        )

        cls._grafo_memoria = g
        return g

    @classmethod
    def obtener_grafo(cls):
        """Devuelve el grafo actual en memoria."""

        if cls._grafo_memoria is None:
            return cls.construir_grafo()

        return cls._grafo_memoria


def cargar_grafo():
    """Construye el grafo semántico al iniciar la aplicación."""
    return SemanticEngine.construir_grafo()
