# Reglas de negocio

## Acceso
- Todas las páginas requieren sesión. Los permisos dependen del rol (`admin`, `profesor`, `alumno`).
- Cada usuario de alumno/profesor está vinculado a su registro con `<ref>` en `usuarios.xml`.
- Las contraseñas se guardan con hash; las consultas XPath usan variables (sin concatenar texto).

## Calificaciones
- Escala de 0 a 100. **70 o más aprueba** (`CALIFICACION_MINIMA` en `config.py`).
- El estatus lo calcula el sistema: ≥ 70 *Aprobado*, < 70 *Reprobado*, sin calificación *Cursando*.
- Un profesor solo califica los grupos que imparte. Si algún dato es inválido no se guarda nada.
- Al calificar se recalcula `alumnos.promedio` (promedio de todas las calificaciones del alumno).
- Un alumno está **en riesgo** si su promedio es menor a 80 (`UMBRAL_RIESGO`).

## Grupos
- Un grupo = una materia + un profesor + periodo + días + horario + aula.
- No se permite que un **profesor** imparta dos grupos que se traslapan (mismos días y horas).
- No se permite que un **aula** esté ocupada por dos grupos al mismo tiempo.
- La hora de fin debe ser posterior a la de inicio. Clases contiguas (09:00–11:00 y 11:00–13:00) no chocan.
- No se puede eliminar un grupo con inscripciones.

## Inscripciones
Para inscribir a un alumno en un grupo debe cumplirse:
1. El alumno existe y su estatus es *Activo*.
2. No tiene esa materia aprobada ni en curso.
3. Tiene aprobados **todos** los prerrequisitos directos de la materia.
4. El grupo no choca en horario con otro grupo que ya cursa.

Solo se pueden dar de baja inscripciones *en curso*; el historial calificado se conserva.

## Integridad al eliminar (el sistema responde 409 con el motivo)
| Registro | No se elimina si… |
|---|---|
| Alumno | tiene inscripciones en su historial o una cuenta vinculada |
| Profesor | imparte grupos, es titular de una materia o tiene cuenta vinculada |
| Materia | tiene grupos, aparece en inscripciones o es prerrequisito de otra |
| Grupo | tiene inscripciones |

## Materias disponibles
- Panel del alumno (Python): materias no aprobadas ni en curso con todos sus prerrequisitos aprobados.
- Consulta SPARQL `materias_disponibles.rq`: igual, pero también lista las que el alumno está cursando
  (elegibles = cumple prerrequisitos y no la ha aprobado).
