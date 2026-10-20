"""Pruebas del módulo de profesores: DTD, XSD, XSLT (HTML y RDF) y SPARQL.

Ejecutar desde la raíz del proyecto:  pytest tests/test_profesores.py -v
"""
import copy
from pathlib import Path

import pytest
from lxml import etree
from rdflib import Graph, Literal, URIRef

ROOT = Path(__file__).resolve().parents[1]
XML = ROOT / "data" / "xml" / "profesores.xml"
DTD = ROOT / "schemas" / "dtd" / "profesores.dtd"
XSD = ROOT / "schemas" / "xsd" / "profesores.xsd"
XSL_HTML = ROOT / "xslt" / "html" / "profesores.xsl"
XSL_RDF = ROOT / "xslt" / "rdf" / "profesores2rdf.xsl"
ONTOLOGIA = ROOT / "ontology" / "academico.ttl"
SPARQL = ROOT / "sparql"

AC = "http://ejemplo.edu/academico#"


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
    assert len(html.xpath("//tbody/tr")) == 14      # 3 de ejemplo + 11 reales (seed_data.py)
    texto = str(html)
    assert "Ana López" in texto
    assert "Sin materias asignadas" in texto     # María García no tiene materias


# ---------- XSLT -> RDF ----------
def test_rdf_numero_de_profesores_y_departamentos(grafo):
    assert len(list(grafo.subjects(predicate=URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type"),
                                   object=URIRef(AC + "Profesor")))) == 14
    deps = set(grafo.subjects(predicate=URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type"),
                              object=URIRef(AC + "Departamento")))
    assert len(deps) == 1      # los 3 profesores son de "Sistemas"


def test_rdf_relacion_imparte(grafo):
    ana = URIRef(AC + "Prof_P1001")
    materias = set(grafo.objects(ana, URIRef(AC + "imparte")))
    assert materias == {URIRef(AC + "Mat_CS201"), URIRef(AC + "Mat_CS205")}


# ---------- SPARQL ----------
def test_sparql_profesores_por_departamento(grafo):
    filas = {str(r.nombre): int(r.numMaterias)
             for r in grafo.query(consulta("profesores_por_departamento.rq"))}
    assert filas == {"Ana López": 2, "Juan Pérez": 1, "María García": 0}


def test_sparql_materias_de_profesor(grafo):
    r = grafo.query(consulta("materias_de_profesor.rq"),
                    initBindings={"profesor": URIRef(AC + "Prof_P1001")})
    assert [str(f.codigo) for f in r] == ["CS201", "CS205"]


def test_sparql_profesores_sin_materias(grafo):
    nombres = [str(f.nombre) for f in grafo.query(consulta("profesores_sin_materias.rq"))]
    assert nombres == ["María García"]


def test_sparql_ruta_inversa(grafo):
    """El grafo solo guarda 'imparte'; con la ruta inversa ^ se obtiene quién imparte la materia
    sin necesidad de un razonador que materialice 'impartidaPor'."""
    q = """PREFIX ac: <http://ejemplo.edu/academico#>
           SELECT ?prof WHERE { ac:Mat_CS105 ^ac:imparte ?prof }"""
    assert [str(f.prof) for f in grafo.query(q)] == [AC + "Prof_P1002"]


def test_sparql_profesores_por_carrera(grafo):
    """Requiere el RDF de materias: aquí se simula con un fragmento."""
    g = Graph()
    for t in grafo:
        g.add(t)
    g.parse(data=f"""
        @prefix ac: <{AC}> .
        ac:Carrera_ISC a ac:Carrera ; ac:codigo "ISC" .
        ac:Mat_CS201 ac:perteneceA ac:Carrera_ISC .
        ac:Mat_CS105 ac:perteneceA ac:Carrera_ISC .
    """, format="turtle")
    r = g.query(consulta("profesores_por_carrera.rq"),
                initBindings={"codigoCarrera": Literal("ISC")})
    assert [str(f.nombre) for f in r] == ["Ana López", "Juan Pérez"]
