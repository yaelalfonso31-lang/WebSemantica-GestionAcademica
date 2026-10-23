# Modelo de datos y grafo

## Relaciones entre los XML
```
usuario.ref ──> alumno | profesor
inscripcion.alumno_id ──> alumno          inscripcion.materia_id ──> materia
inscripcion.grupo_id  ──> grupo           grupo.materia_id ──> materia
grupo.profesor_id ──> profesor            materia.prerrequisito@ref ──> materia
```

## Vocabulario RDF (`http://academico.edu.mx/ontologia#`, prefijo `acad:`)
Recursos: `…/recurso/{alumno|profesor|materia|carrera|inscripcion}/<id>`

| Clase | Propiedades principales |
|---|---|
| `acad:Alumno` | id, matricula, nombre, apellidos, correo, semestre, promedio, estatus, cursaMateria, **aproboMateria** |
| `acad:Materia` | id, clave, nombre, creditos, semestre, perteneceACarrera, impartidaPor, **tienePrerrequisito** (transitiva) |
| `acad:Profesor` | id, nombre, especialidad, correo, departamento, imparte |
| `acad:Inscripcion` | id, periodo, estatus, grupo, calificacionFinal, realizadaPor, inscribeA |

`aproboMateria` se deriva de las inscripciones con estatus *Aprobado* (no se escribe a mano).
La transitividad de prerrequisitos se consulta con la ruta de propiedad `acad:tienePrerrequisito+`
(SPARQL 1.1), sin necesidad de un razonador.
