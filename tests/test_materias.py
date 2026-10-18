"""Pruebas del módulo de materias: DTD, XSD (ID/IDREF), XSLT (HTML y RDF) y SPARQL (tienePrerrequisito+).

Ejecutar desde la raíz del proyecto:  pytest tests/test_materias.py -v
"""
import copy
from pathlib import Path
import pytest
from lxml import etree
from rdflib import Graph, URIRef

ROOT = Path(__file__).resolve().parents[1]
XML = ROOT / "data" / "xml" / "materias.xml"
XML_ALUMNOS = ROOT / "data" / "xml" / "alumnos.xml"
DTD = ROOT / "schemas" / "dtd" / "materias.dtd"
XSD = ROOT / "schemas" / "xsd" / "materias.xsd"
XSL_HTML = ROOT / "xslt" / "html" / "materias.xsl"
XSL_RDF = ROOT / "xslt" / "rdf" / "materias2rdf.xsl"
XSL_ALUMNOS_RDF = ROOT / "xslt" / "rdf" / "alumnos2rdf.xsl"
ONTOLOGIA = ROOT / "ontology" / "academico.ttl"
REGLAS = ROOT / "ontology" / "reglas.ttl"
SPARQL = ROOT / "sparql"

ACAD = "http://academico.edu.mx/ontologia#"
RECURSO_MAT = "http://academico.edu.mx/recurso/materia/"


@pytest.fixture
def doc():
    return etree.parse(str(XML))


@pytest.fixture(scope="module")
def xsd():
    return etree.XMLSchema(etree.parse(str(XSD)))


@pytest.fixture(scope="module")
def grafo():
    g = Graph()
    if ONTOLOGIA.exists():
        g.parse(str(ONTOLOGIA), format="turtle")
    if REGLAS.exists() and REGLAS.stat().st_size > 0:
        g.parse(str(REGLAS), format="turtle")

    rdf_materias = etree.XSLT(etree.parse(str(XSL_RDF)))(etree.parse(str(XML)))
    g.parse(data=etree.tostring(rdf_materias), format="xml")

    if XML_ALUMNOS.exists() and XSL_ALUMNOS_RDF.exists():
        rdf_alumnos = etree.XSLT(etree.parse(str(XSL_ALUMNOS_RDF)))(etree.parse(str(XML_ALUMNOS)))
        g.parse(data=etree.tostring(rdf_alumnos), format="xml")
    return g


# ---------- 1. Validación DTD ----------
def test_dtd_acepta_materias_xml(doc):
    dtd = etree.DTD(str(DTD))
    assert dtd.validate(doc), dtd.error_log


def test_dtd_rechaza_prerrequisito_huerfano(doc):
    malo = copy.deepcopy(doc)
    prerreq = malo.find(".//prerrequisito")
    prerreq.set("ref", "CCOS999")  # ID que no existe en el catálogo
    dtd = etree.DTD(str(DTD))
    assert not dtd.validate(malo)


# ---------- 2. Validación XSD ----------
def test_xsd_acepta_materias_xml(doc, xsd):
    assert xsd.validate(doc), xsd.error_log


def test_xsd_rechaza_id_duplicado(doc, xsd):
    malo = copy.deepcopy(doc)
    materias = malo.findall("materia")
    materias[1].set("id", materias[0].get("id"))
    assert not xsd.validate(malo)


def test_xsd_rechaza_ref_prerrequisito_inexistente(doc, xsd):
    malo = copy.deepcopy(doc)
    prerreq = malo.find(".//prerrequisito")
    prerreq.set("ref", "ICCS999")
    assert not xsd.validate(malo)


# ---------- 3. Transformación XSLT -> HTML ----------
def test_xslt_html_genera_catalogo_materias(doc):
    html = etree.XSLT(etree.parse(str(XSL_HTML)))(doc)
    assert len(html.xpath("//tbody/tr")) == 12
    assert "Sistemas Operativos II" in str(html)


# ---------- 4. Transformación XSLT -> RDF y Consultas SPARQL (tienePrerrequisito+) ----------
def test_sparql_prerrequisitos_transitivos(grafo):
    query = (SPARQL / "prerrequisitos_de_materia.rq").read_text(encoding="utf-8")
    resultados = list(grafo.query(query))

    # Filtrar resultados para CCOS254 (Sistemas Operativos II)
    prerreqs_so2 = {str(r.prerrequisitoId): str(r.tipo) for r in resultados if str(r.materiaId) == "CCOS254"}
    # Debe encontrar CCOS252 como Directo y CCOS013 como Transitivo
    assert prerreqs_so2 == {
        "CCOS252": "Directo",
        "CCOS013": "Transitivo"
    }

    # Filtrar resultados para ICCS250 (Circuitos Electrónicos)
    prerreqs_ce = {str(r.prerrequisitoId): str(r.tipo) for r in resultados if str(r.materiaId) == "ICCS250"}
    assert prerreqs_ce == {
        "ICCS007": "Directo",
        "ICCS004": "Transitivo"
    }


def test_sparql_materias_disponibles_ruta_transitiva(grafo):
    query = (SPARQL / "materias_disponibles.rq").read_text(encoding="utf-8")
    resultados = list(grafo.query(query))

    # A003 (Laura) aprobó CCOS013, por lo que puede cursar CCOS252 (SO I), pero NO CCOS254 (SO II)
    disp_a003 = {str(r.materiaId) for r in resultados if str(r.alumnoId) == "A003"}
    assert "CCOS252" in disp_a003
    assert "CCOS254" not in disp_a003

    # A002 (Carlos) aprobó tanto CCOS013 como CCOS252, por lo que SÍ puede cursar CCOS254 (SO II)
    disp_a002 = {str(r.materiaId) for r in resultados if str(r.alumnoId) == "A002"}
    assert "CCOS254" in disp_a002