"""Pruebas del módulo de profesores: DTD, XSD, XSLT (HTML y RDF) y SPARQL.

Ejecutar desde la raíz del proyecto:  pytest tests/test_profesores.py -v
"""
import copy
from pathlib import Path

import pytest
from lxml import etree
from rdflib import Graph, Literal, URIRef

ROOT = Path(__file__).resolve().parents[1]
XML = ROOT / "tests" / "fixtures" / "xml" / "profesores_ejemplo.xml"   # 3 profesores de muestra (P1001-P1003)
DTD = ROOT / "schemas" / "dtd" / "profesores.dtd"
XSD = ROOT / "schemas" / "xsd" / "profesores.xsd"
XSL_HTML = ROOT / "xslt" / "html" / "profesores.xsl"
XSL_RDF = ROOT / "xslt" / "rdf" / "profesores2rdf.xsl"
ONTOLOGIA = ROOT / "ontology" / "academico.ttl"
SPARQL = ROOT / "sparql"

AC = "http://academico.edu.mx/ontologia#"
RP = "http://academico.edu.mx/recurso/profesor/"
RM = "http://academico.edu.mx/recurso/materia/"


# ---------- utilidades ----------
@pytest.fixture
def doc():
    return etree.parse(str(XML))


@pytest.fixture(scope="module")
def xsd():
    return etree.XMLSchema(etree.parse(str(XSD)))


def consulta(nombre: str) -> str:
    return (SPARQL / nombre).read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def grafo():
    resultado = etree.XSLT(etree.parse(str(XSL_RDF)))(etree.parse(str(XML)))
    g = Graph()
    g.parse(str(ONTOLOGIA), format="turtle")
    g.parse(data=etree.tostring(resultado), format="xml")
    return g


# ---------- DTD ----------
def test_dtd_acepta_el_xml(doc):
    dtd = etree.DTD(str(DTD))
    assert dtd.validate(doc), dtd.error_log


def test_dtd_rechaza_profesor_sin_correo(doc):
    malo = copy.deepcopy(doc)
    p = malo.find("profesor")
    p.remove(p.find("correo"))
    assert not etree.DTD(str(DTD)).validate(malo)


# ---------- XSD ----------
def test_xsd_acepta_el_xml(doc, xsd):
    assert xsd.validate(doc), xsd.error_log


@pytest.mark.parametrize("campo,xpath,valor", [
    ("correo inválido", ".//correo", "no-es-correo"),
    ("nombre vacío", ".//nombre", "   "),
])
def test_xsd_rechaza_textos_invalidos(doc, xsd, campo, xpath, valor):
    malo = copy.deepcopy(doc)
    malo.find(xpath).text = valor
    assert not xsd.validate(malo), campo


def test_xsd_rechaza_codigo_de_materia_invalido(doc, xsd):
    malo = copy.deepcopy(doc)
    malo.find(".//materia").set("codigo", "cs20")
    assert not xsd.validate(malo)


def test_xsd_rechaza_id_con_formato_invalido(doc, xsd):
    malo = copy.deepcopy(doc)
    malo.find("profesor").set("id", "P12")
    assert not xsd.validate(malo)


def test_xsd_rechaza_correo_duplicado(doc, xsd):
    malo = copy.deepcopy(doc)
    correos = malo.findall(".//correo")
    correos[1].text = correos[0].text
    assert not xsd.validate(malo)


def test_xsd_permite_profesor_sin_materias(doc, xsd):
    assert doc.xpath("count(//profesor[not(materias_impartidas/materia)])") == 1
    assert xsd.validate(doc)


# ---------- XSLT -> HTML ----------
def test_xslt_html_genera_una_fila_por_profesor(doc):
    html = etree.XSLT(etree.parse(str(XSL_HTML)))(doc)
    assert len(html.xpath("//tbody/tr")) == len(doc.xpath("//profesor"))
    texto = str(html)
    assert "Ana López" in texto
    assert "Sin materias asignadas" in texto     # María García no tiene materias


# ---------- XSLT -> RDF (vocabulario acad: unificado con el resto del sistema) ----------
RDF_TYPE = URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type")


def test_rdf_numero_de_profesores_y_departamentos(grafo):
    assert len(set(grafo.subjects(RDF_TYPE, URIRef(AC + "Profesor")))) == 3
    assert {str(o) for o in grafo.objects(None, URIRef(AC + "departamento"))} == {"Sistemas"}


def test_rdf_usa_las_mismas_uris_que_materias(grafo):
    """El profesor se identifica igual que en materias2rdf (recurso/profesor/<id>)."""
    assert (URIRef(RP + "P1001"), RDF_TYPE, URIRef(AC + "Profesor")) in grafo


def test_rdf_relacion_imparte(grafo):
    materias = set(grafo.objects(URIRef(RP + "P1001"), URIRef(AC + "imparte")))
    assert materias == {URIRef(RM + "CS201"), URIRef(RM + "CS205")}


# ---------- SPARQL ----------
def test_sparql_profesores_por_departamento(grafo):
    filas = {str(r.nombre): int(r.numMaterias) for r in grafo.query(consulta("profesores_por_departamento.rq"))}
    assert filas == {"Ana López": 2, "Juan Pérez": 1, "María García": 0}


def test_sparql_materias_de_profesor(grafo):
    r = grafo.query(consulta("materias_de_profesor.rq"), initBindings={"profesor": URIRef(RP + "P1001")})
    assert [str(f.codigo) for f in r] == ["CS201", "CS205"]


def test_sparql_profesores_sin_materias(grafo):
    nombres = [str(f.nombre) for f in grafo.query(consulta("profesores_sin_materias.rq"))]
    assert nombres == ["María García"]


def test_sparql_ruta_inversa(grafo):
    """Con la ruta inversa ^ se obtiene quién imparte la materia sin materializar 'impartidaPor'."""
    q = f"PREFIX acad: <{AC}> SELECT ?prof WHERE {{ <{RM}CS105> ^acad:imparte ?prof }}"
    assert [str(f.prof) for f in grafo.query(q)] == [RP + "P1002"]


def test_sparql_profesores_por_carrera(grafo):
    """Se combina con el RDF de materias: aquí se simula con un fragmento."""
    g = Graph()
    for t in grafo:
        g.add(t)
    g.parse(data=f"""
        @prefix acad: <{AC}> .
        <{RM}CS201> acad:perteneceACarrera <http://academico.edu.mx/recurso/carrera/ISC> .
        <{RM}CS105> acad:perteneceACarrera <http://academico.edu.mx/recurso/carrera/ISC> .
    """, format="turtle")
    r = g.query(consulta("profesores_por_carrera.rq"))
    assert [(str(f.carrera), str(f.nombre)) for f in r] == [("ISC", "Ana López"), ("ISC", "Juan Pérez")]
