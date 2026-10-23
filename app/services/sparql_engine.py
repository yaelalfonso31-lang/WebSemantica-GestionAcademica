import os
import re

from rdflib import Literal

from app.services.paths import ruta
from app.services.rdf_graph import SemanticEngine

# Solo nombres simples dentro de sparql/: impide rutas como ../../config.py
_NOMBRE_CONSULTA = re.compile(r'^[A-Za-z0-9_]+\.rq$')


class SPARQLEngine:
    @staticmethod
    def listar_consultas():
        directorio = ruta('SPARQL_DIR')
        return sorted(f for f in os.listdir(directorio)
                      if _NOMBRE_CONSULTA.match(f) and os.path.getsize(os.path.join(directorio, f)) > 0)

    @staticmethod
    def ejecutar_consulta(archivo_rq, parametros=None):
        """Lee un .rq de sparql/, enlaza parámetros de forma segura y ejecuta sobre el grafo."""
        if not isinstance(archivo_rq, str) or not _NOMBRE_CONSULTA.match(archivo_rq):
            raise ValueError('Nombre de consulta no válido.')

        ruta_rq = ruta('SPARQL_DIR', archivo_rq)
        if not os.path.exists(ruta_rq):
            raise FileNotFoundError(f'No se encontró la consulta: {archivo_rq}')

        with open(ruta_rq, 'r', encoding='utf-8') as f:
            query_string = f.read()
        if not query_string.strip():
            raise ValueError(f'La consulta {archivo_rq} está vacía.')

        # initBindings enlaza valores como literales
        bindings = {k: Literal(v) for k, v in (parametros or {}).items()}

        g = SemanticEngine.obtener_grafo()
        try:
            resultados_crudos = g.query(query_string, initBindings=bindings)
        except Exception as e:
            raise ValueError(f'Error de sintaxis SPARQL: {e}')

        lista_resultados = []
        for fila in resultados_crudos:
            lista_resultados.append({
                str(var): ('' if fila[var] is None else str(fila[var]))
                for var in resultados_crudos.vars
            })
        return lista_resultados
