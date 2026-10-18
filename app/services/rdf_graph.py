import os
from lxml import etree
from rdflib import Graph
from flask import current_app


class SemanticEngine:
    _grafo_memoria = None

    @classmethod
    def transformar_xml_a_rdf(cls, xml_filename, xslt_filename, output_rdf_filename):
        """Transforma un archivo XML a RDF/XML utilizando XSLT y lxml."""

        xml_dir = current_app.config.get("XML_DIR", "data/xml")
        rdf_dir = current_app.config.get("RDF_DIR", "data/rdf")

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
            # Leer el XML y la hoja de transformación
            xml_doc = etree.parse(xml_path)
            xslt_doc = etree.parse(xslt_path)
            transform = etree.XSLT(xslt_doc)

            # Transformar XML a RDF/XML
            rdf_result = transform(xml_doc)

            # Crear el directorio de salida si no existe
            os.makedirs(rdf_dir, exist_ok=True)

            # Guardar el RDF generado
            rdf_result.write(
                output_path,
                encoding="UTF-8",
                xml_declaration=True,
                pretty_print=True
            )

            print(f"RDF generado correctamente: {output_path}")
            return output_path

        except (etree.XMLSyntaxError, etree.XSLTParseError,
                etree.XSLTApplyError, OSError) as error:
            print(
                f"Error al transformar {xml_filename} "
                f"con {xslt_filename}: {error}"
            )
            return None

    @classmethod
    def construir_grafo(cls):
        """Construye el grafo RDF uniendo la ontología y los datos académicos."""

        g = Graph()

        # 1. Cargar la ontología y las reglas semánticas
        onto_path = os.path.join("ontology", "academico.ttl")
        reglas_path = os.path.join("ontology", "reglas.ttl")

        if os.path.exists(onto_path):
            g.parse(onto_path, format="turtle")
        else:
            print(f"Advertencia: No se encontró la ontología: {onto_path}")

        if os.path.exists(reglas_path):
            g.parse(reglas_path, format="turtle")
        else:
            print(f"Advertencia: No se encontraron las reglas: {reglas_path}")

        # 2. Transformar los XML académicos a RDF/XML
        transformaciones = [
            ("alumnos.xml", "alumnos2rdf.xsl", "alumnos.rdf"),
            ("profesores.xml", "profesores2rdf.xsl", "profesores.rdf"),
        ]

        # 3. Incorporar cada RDF generado al grafo maestro
        for xml_filename, xslt_filename, rdf_filename in transformaciones:
            rdf_path = cls.transformar_xml_a_rdf(
                xml_filename,
                xslt_filename,
                rdf_filename
            )

            if rdf_path and os.path.exists(rdf_path):
                try:
                    g.parse(rdf_path, format="xml")
                    print(f"RDF incorporado al grafo: {rdf_filename}")
                except Exception as error:
                    print(
                        f"Error al cargar {rdf_filename} en el grafo: {error}"
                    )

        # 4. Serializar el grafo completo
        rdf_dir = current_app.config.get("RDF_DIR", "data/rdf")
        os.makedirs(rdf_dir, exist_ok=True)

        grafo_completo_path = os.path.join(
            rdf_dir,
            "grafo_completo.ttl"
        )

        g.serialize(
            destination=grafo_completo_path,
            format="turtle"
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


# Función global que llama al iniciar la aplicación
def cargar_grafo():
    return SemanticEngine.construir_grafo()
