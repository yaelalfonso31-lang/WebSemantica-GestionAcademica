<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

    <!-- Importamos el layout que controla el menú, CSS estático y JavaScript -->
    <xsl:import href="layout.xsl"/>

    <xsl:template name="content">
        <html lang="es">
            <head>
                <meta charset="UTF-8" />
                <title>Sistema Semántico Académico</title>
                <link rel="stylesheet" type="text/css" href="/static/css/alumnos.css" />
                <style>
                    .tabla-contenedor { max-height: none !important; overflow-y: visible !important; }
                    .lista-prerreq { margin: 0; padding-left: 0; list-style: none; }
                    .lista-prerreq li { margin-bottom: 4px; }
                    .badge-prerreq { background: #e0e7ff; color: #1e40af; padding: 2px 8px; border-radius: 4px; font-size: 0.8em; font-weight: bold; margin-right: 6px; display: inline-block; }
                </style>
            </head>
            <body class="cuerpo-alumnos">
                <div class="pagina-alumnos">

                    <!-- Header con Botón Nueva Materia -->
                    <div class="encabezado-modulo">
                        <header>
                            <h1 class="titulo-modulo">Módulo de Materias</h1>
                            <p class="subtitulo-modulo">EduSemantic - Sistema Web Semántico de Gestión Académica</p>
                        </header>
                        <button onclick="abrirModalMateria()" class="boton boton-primario">
                            + Nueva Materia
                        </button>
                    </div>

                    <!-- Resumen rápido con XPath -->
                    <div class="resumen-alumnos">
                        <div class="tarjeta-resumen">
                            <span class="etiqueta-resumen">Total de Materias</span>
                            <p class="valor-resumen valor-azul">
                                <xsl:value-of select="count(materias/materia)"/>
                            </p>
                        </div>
                        <div class="tarjeta-resumen">
                            <span class="etiqueta-resumen">Total de Créditos</span>
                            <p class="valor-resumen valor-verde">
                                <xsl:value-of select="sum(materias/materia/creditos)"/>
                            </p>
                        </div>
                        <div class="tarjeta-resumen">
                            <span class="etiqueta-resumen">Materias con Seriación</span>
                            <p class="valor-resumen valor-indigo">
                                <xsl:value-of select="count(materias/materia[prerrequisitos/prerrequisito])"/>
                            </p>
                        </div>
                    </div>

                    <!-- Contenedor de la tabla -->
                    <div class="tabla-contenedor">
                        <table class="tabla-alumnos">
                            <thead class="tabla-encabezado">
                                <tr>
                                    <th scope="col" class="celda-encabezado">Clave / ID</th>
                                    <th scope="col" class="celda-encabezado">Asignatura</th>
                                    <th scope="col" class="celda-encabezado">Semestre / Créditos</th>
                                    <th scope="col" class="celda-encabezado">Carrera</th>
                                    <th scope="col" class="celda-encabezado">Profesor</th>
                                    <th scope="col" class="celda-encabezado">Prerrequisitos</th>
                                    <th scope="col" class="celda-encabezado texto-derecha">Acciones</th>
                                </tr>
                            </thead>
                            <tbody class="tabla-cuerpo">
                                <xsl:for-each select="materias/materia">
                                    <xsl:sort select="semestre" data-type="number"/>
                                    <tr class="fila-alumno">

                                        <!-- Clave e ID -->
                                        <td class="celda-alumno">
                                            <div class="matricula-alumno">
                                                <xsl:value-of select="@clave"/>
                                            </div>
                                            <div class="id-alumno">
                                                ID: <xsl:value-of select="@id"/>
                                            </div>
                                        </td>

                                        <!-- Nombre y Descripción -->
                                        <td class="celda-alumno">
                                            <div class="nombre-alumno">
                                                <xsl:value-of select="normalize-space(nombre)"/>
                                            </div>
                                            <div class="correo-alumno">
                                                <xsl:value-of select="normalize-space(descripcion)"/>
                                            </div>
                                        </td>

                                        <!-- Semestre y Créditos -->
                                        <td class="celda-alumno texto-secundario">
                                            <div>Semestre <xsl:value-of select="normalize-space(semestre)"/></div>
                                            <div class="id-alumno"><xsl:value-of select="normalize-space(creditos)"/> créditos</div>
                                        </td>

                                        <!-- Carrera -->
                                        <td class="celda-alumno">
                                            <span class="etiqueta-carrera">
                                                <xsl:value-of select="carrera/@codigo"/>
                                            </span>
                                        </td>

                                        <!-- Profesor -->
                                        <td class="celda-alumno">
                                            <div class="nombre-alumno">
                                                <xsl:value-of select="normalize-space(profesor)"/>
                                            </div>
                                            <div class="id-alumno">
                                                ID: <xsl:value-of select="profesor/@id"/>
                                            </div>
                                        </td>

                                        <!-- Prerrequisitos -->
                                        <td class="celda-alumno">
                                            <xsl:choose>
                                                <xsl:when test="prerrequisitos/prerrequisito">
                                                    <ul class="lista-prerreq">
                                                        <xsl:for-each select="prerrequisitos/prerrequisito">
                                                            <li>
                                                                <span class="badge-prerreq"><xsl:value-of select="@ref"/></span>
                                                                <xsl:value-of select="@nombre"/>
                                                            </li>
                                                        </xsl:for-each>
                                                    </ul>
                                                </xsl:when>
                                                <xsl:otherwise>
                                                    <span class="texto-secundario">Ninguno</span>
                                                </xsl:otherwise>
                                            </xsl:choose>
                                        </td>

                                        <!-- Botón Eliminar -->
                                        <td class="celda-alumno texto-derecha">
                                            <button onclick="eliminarMateria('{@id}')" class="boton boton-peligro boton-pequeno">
                                                Eliminar
                                            </button>
                                        </td>

                                    </tr>
                                </xsl:for-each>
                            </tbody>
                        </table>
                    </div>

                    <!-- MODAL NUEVA MATERIA -->
                    <div id="modalNuevaMateria" class="modal-overlay hidden">
                        <div class="modal-contenido">
                            <div class="modal-encabezado">
                                <h3 class="modal-titulo">Registrar Nueva Materia</h3>
                                <button onclick="cerrarModalMateria()" class="boton-cerrar">&#215;</button>
                            </div>

                            <form id="formNuevaMateria" onsubmit="guardarMateria(event)">
                                <div class="formulario-grid formulario-dos-columnas espacio-inferior">
                                    <div>
                                        <label class="etiqueta-campo">ID de la Materia</label>
                                        <input type="text" id="mat_id" pattern="(CCOS|ICCS)[0-9]{{3}}" placeholder="Ej. CCOS260" required="required" class="campo-formulario"/>
                                    </div>
                                    <div>
                                        <label class="etiqueta-campo">Clave</label>
                                        <input type="text" id="mat_clave" pattern="(CCOS|ICCS) [0-9]{{3}}" placeholder="Ej. CCOS 260" required="required" class="campo-formulario"/>
                                    </div>
                                </div>
                                <div class="grupo-campo espacio-inferior">
                                    <label class="etiqueta-campo">Nombre de la Asignatura</label>
                                    <input type="text" id="mat_nombre" required="required" class="campo-formulario"/>
                                </div>
                                <div class="grupo-campo espacio-inferior">
                                    <label class="etiqueta-campo">Descripción</label>
                                    <input type="text" id="mat_descripcion" required="required" class="campo-formulario"/>
                                </div>
                                <div class="formulario-grid formulario-dos-columnas espacio-inferior">
                                    <div>
                                        <label class="etiqueta-campo">Créditos (1 - 10)</label>
                                        <input type="number" id="mat_creditos" min="1" max="10" value="6" required="required" class="campo-formulario"/>
                                    </div>
                                    <div>
                                        <label class="etiqueta-campo">Semestre (1 - 10)</label>
                                        <input type="number" id="mat_semestre" min="1" max="10" value="5" required="required" class="campo-formulario"/>
                                    </div>
                                </div>
                                <div class="formulario-grid formulario-dos-columnas espacio-inferior">
                                    <div>
                                        <label class="etiqueta-campo">ID Profesor</label>
                                        <input type="text" id="mat_profesor_id" pattern="P[0-9]{{3}}" placeholder="Ej. P001" value="P001" required="required" class="campo-formulario"/>
                                    </div>
                                    <div>
                                        <label class="etiqueta-campo">Nombre del Profesor</label>
                                        <input type="text" id="mat_profesor_nombre" required="required" class="campo-formulario"/>
                                    </div>
                                </div>
                                <div class="grupo-campo espacio-inferior-grande">
                                    <label class="etiqueta-campo">Prerrequisitos (Ctrl + Clic para varios)</label>
                                    <select id="mat_prerrequisitos" multiple="multiple" size="4" class="campo-formulario">
                                        <xsl:for-each select="materias/materia">
                                            <option value="{@id}">
                                                <xsl:value-of select="@id"/> - <xsl:value-of select="normalize-space(nombre)"/>
                                            </option>
                                        </xsl:for-each>
                                    </select>
                                </div>
                                <div class="acciones-formulario">
                                    <button type="button" onclick="cerrarModalMateria()" class="boton boton-secundario">Cancelar</button>
                                    <button type="submit" class="boton boton-exito">Guardar Materia</button>
                                </div>
                            </form>
                        </div>
                    </div>

                </div>

                <script>
                    function abrirModalMateria() {
                        document.getElementById('modalNuevaMateria').classList.remove('hidden');
                    }
                    function cerrarModalMateria() {
                        document.getElementById('modalNuevaMateria').classList.add('hidden');
                    }
                    async function guardarMateria(e) {
                        e.preventDefault();
                        const selectPrerreq = document.getElementById('mat_prerrequisitos');
                        const prerrequisitos = Array.from(selectPrerreq.selectedOptions).map(opt => opt.value);

                        const payload = {
                            id: document.getElementById('mat_id').value.trim(),
                            clave: document.getElementById('mat_clave').value.trim(),
                            nombre: document.getElementById('mat_nombre').value.trim(),
                            descripcion: document.getElementById('mat_descripcion').value.trim(),
                            creditos: document.getElementById('mat_creditos').value,
                            semestre: document.getElementById('mat_semestre').value,
                            carrera_codigo: "ICC",
                            carrera_nombre: "Ingeniería en Ciencias de la Computación",
                            profesor_id: document.getElementById('mat_profesor_id').value.trim(),
                            profesor_nombre: document.getElementById('mat_profesor_nombre').value.trim(),
                            prerrequisitos: prerrequisitos
                        };

                        const resp = await fetch('/api/materias', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify(payload)
                        });
                        const data = await resp.json();
                        if (resp.ok) {
                            window.location.reload();
                        } else {
                            alert(data.error || 'Error de validación al guardar materia');
                        }
                    }
                    async function eliminarMateria(id) {
                        if (!confirm('¿Deseas eliminar la materia ' + id + '?')) return;
                        const resp = await fetch('/api/materias/' + id, { method: 'DELETE' });
                        const data = await resp.json();
                        if (resp.ok) {
                            window.location.reload();
                        } else {
                            alert(data.error || 'Error al eliminar materia');
                        }
                    }
                </script>
            </body>
        </html>
    </xsl:template>
</xsl:stylesheet>