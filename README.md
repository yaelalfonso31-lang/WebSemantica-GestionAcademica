# EduSemantic – Sistema académico (Flask + XML/XSLT + RDF/SPARQL)

## Arranque
    pip install -r requirements.txt
    python scripts/seed_data.py      # (opcional) regenera datos de ejemplo coherentes
    python run.py                    # FLASK_DEBUG=1 para modo debug
    pytest

Variables de entorno: `SECRET_KEY` (obligatoria en producción), `SESSION_COOKIE_SECURE=1` (con HTTPS).

## Cuentas de ejemplo (contraseña `1234`, solo desarrollo)
| usuario | rol | vinculado a |
|---|---|---|
| admin | admin | — |
| profe | profesor | P012 (Eduardo Profesor) |
| alumno | alumno | A006 (Yael Serrano) |

Cada usuario de `usuarios.xml` lleva `<ref>` con el ID de su registro en `alumnos.xml` / `profesores.xml`.
Los alumnos ven su kardex y horario; los profesores sus grupos (`grupos.xml`) y solo pueden calificar los suyos.

## Modelo de datos (IDs que deben coincidir)
usuario.ref → alumno/profesor · inscripcion.alumno_id → alumno · inscripcion.materia_id → materia ·
inscripcion.grupo_id → grupo · grupo.materia_id → materia · grupo.profesor_id → profesor.

## Datos de ejemplo
- `python scripts/seed_data.py` — crea un conjunto base coherente (sobrescribe usuarios, grupos e inscripciones; deja respaldo).
- `python scripts/ampliar_datos.py` — **agrega** más materias, profesores, alumnos, grupos e inscripciones sin borrar nada
  (`--dry-run` para solo ver qué haría). Cada alta se valida con las reglas del sistema (prerrequisitos, choques de horario).
  Los profesores y alumnos añadidos son ficticios.

## Qué hace cada rol
| Rol | Secciones |
|---|---|
| admin | Alumnos, Profesores, Materias, **Grupos** (crear grupos, inscribir y dar de baja), SPARQL |
| profesor | Mis Grupos, Calificaciones, **Mi Horario** (calendario semanal) |
| alumno | Mi Kardex, **Mi Horario** (calendario semanal), panel con materias que puede cursar |

Reglas completas en `docs/reglas_de_negocio.md`.

## Pruebas
`pytest` — usan una copia de `tests/fixtures/xml`, por lo que no dependen ni modifican tu `data/`.
