import os
from app.services.rdf_graph import SemanticEngine

class SPARQLEngine:
    @staticmethod
    def ejecutar_consulta(archivo_rq, parametros=None):
        """Lee un archivo .rq, reemplaza parámetros y ejecuta la consulta sobre el grafo."""
        ruta_rq = os.path.join('sparql', archivo_rq)
        
        if not os.path.exists(ruta_rq):
            raise FileNotFoundError(f"No se encontró el archivo de consulta: {ruta_rq}")

        # Leer la consulta SPARQL
        with open(ruta_rq, 'r', encoding='utf-8') as f:
            query_string = f.read()

        # Inyectar parámetros si existen (ej. reemplazar ?carrera_param por "C001")
        if parametros:
            for clave, valor in parametros.items():
                query_string = query_string.replace(f"?{clave}", f'"{valor}"')

        # Obtener el grafo RDF actualizado en memoria
        g = SemanticEngine.obtener_grafo()

        # Ejecutar la consulta
        try:
            resultados_crudos = g.query(query_string)
        except Exception as e:
            raise ValueError(f"Error de sintaxis SPARQL: {e}")

        # Formatear los resultados a una lista de diccionarios para facilitar su uso
        lista_resultados = []
        for fila in resultados_crudos:
            fila_dict = {}
            for var in resultados_crudos.vars:
                valor = fila[var]
                # Extraer solo el valor, ignorando URIs completas si es un literal simple
                fila_dict[str(var)] = str(valor) if valor else ""
            lista_resultados.append(fila_dict)

        return lista_resultados