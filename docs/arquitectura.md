# Arquitectura

```
Navegador ──> Flask (rutas + auth) ──> servicios ──> XML + esquemas + XSLT ──> RDF / SPARQL
```

| Capa | Dónde | Qué hace |
|---|---|---|
| Presentación | `xslt/html/`, `app/static/` | Las vistas se generan aplicando XSLT a XML; Bootstrap + CSS propio. |
| Rutas y permisos | `app/routes/`, `app/auth/` | Atienden peticiones y aplican `login_requerido` / `rol_requerido`. |
| Reglas | `app/services/academic_metrics.py`, `asignaciones.py` | Quién ve qué, horarios, métricas, prerrequisitos, choques. |
| Datos | `app/services/xml_repository.py`, `data/xml/` | CRUD con validación DTD+XSD, respaldo y escritura atómica. |
| Semántica | `app/services/rdf_graph.py`, `sparql_engine.py`, `xslt/rdf/`, `ontology/`, `sparql/` | XML → RDF → grafo → consultas SPARQL. |

Flujo de guardado: modificar en memoria → validar XSD y DTD → respaldo → escribir archivo temporal → reemplazar → reconstruir grafo.

Scripts útiles: `scripts/seed_data.py` (datos base coherentes), `scripts/ampliar_datos.py` (agrega más datos sin borrar nada),
`scripts/validate_all.py` y `scripts/build_rdf.py`.
