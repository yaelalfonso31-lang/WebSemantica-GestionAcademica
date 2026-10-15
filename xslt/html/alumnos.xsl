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

            </head>
            <body class="cuerpo-alumnos">
                <div class="pagina-alumnos">


                    <!-- Header con Botón Nuevo Alumno -->
                    <div class="encabezado-modulo">
                        <header>
                            <h1 class="titulo-modulo">Módulo de Alumnos</h1>
                            <p class="subtitulo-modulo">EduSemantic - Sistema Web Semántico de Gestión Académica</p>
                        </header>
                        <button onclick="abrirModal()" class="boton boton-primario">
                    + Nuevo Alumno
                        </button>
                    </div>

                    <!-- Resumen rápido con XPath -->
                    <div class="resumen-alumnos">
                        <div class="tarjeta-resumen">
                            <span class="etiqueta-resumen">Total de Alumnos</span>
                            <p class="valor-resumen valor-azul">
                                <xsl:value-of select="count(alumnos/alumno)"/>
                            </p>
                        </div>
                        <div class="tarjeta-resumen">
                            <span class="etiqueta-resumen">Promedio General</span>
                            <p class="valor-resumen valor-verde">
                                <xsl:choose>
                                    <xsl:when test="count(alumnos/alumno) &gt; 0">
                                        <xsl:value-of select="format-number(sum(alumnos/alumno/promedio) div count(alumnos/alumno), '0.0')"/>
                                    </xsl:when>
                                    <xsl:otherwise>0.0</xsl:otherwise>
                                </xsl:choose>
                            </p>
                        </div>
                        <div class="tarjeta-resumen">
                            <span class="etiqueta-resumen">Alumnos Activos</span>
                            <p class="valor-resumen valor-indigo">
                                <xsl:value-of select="count(alumnos/alumno[estatus='Activo'])"/>
                            </p>
                        </div>
                    </div>

                    <!-- Contenedor de la tabla -->
                    <div class="tabla-contenedor">
                        <table class="tabla-alumnos">
                            <thead class="tabla-encabezado">
                                <tr>
                                    <th scope="col" class="celda-encabezado">ID / Matrícula</th>
                                    <th scope="col" class="celda-encabezado">Alumno</th>
                                    <th scope="col" class="celda-encabezado">Carrera ID</th>
                                    <th scope="col" class="celda-encabezado">Semestre</th>
                                    <th scope="col" class="celda-encabezado">Promedio</th>
                                    <th scope="col" class="celda-encabezado">Estatus</th>
                                    <th scope="col" class="celda-encabezado texto-derecha">Acciones</th>
                                </tr>
                            </thead>
                            <tbody class="tabla-cuerpo">

                                <xsl:for-each select="alumnos/alumno">
                                    <tr class="fila-alumno">

                                        <!-- ID y Matrícula -->
                                        <td class="celda-alumno">
                                            <div class="matricula-alumno">
                                                <xsl:value-of select="@matricula"/>
                                            </div>
                                            <div class="id-alumno">
                                        ID: <xsl:value-of select="@id"/>
                                            </div>
                                        </td>

                                        <!-- Nombre y Correo -->
                                        <td class="celda-alumno">
                                            <div class="nombre-alumno">
                                                <xsl:value-of select="nombre"/>
                                                <xsl:text></xsl:text>
                                                <xsl:value-of select="apellidos"/>
                                            </div>
                                            <div class="correo-alumno">
                                                <xsl:value-of select="correo"/>
                                            </div>
                                        </td>

                                        <!-- Carrera ID -->
                                        <td class="celda-alumno">
                                            <span class="etiqueta-carrera">
                                                <xsl:value-of select="carrera_id"/>
                                            </span>
                                        </td>

                                        <!-- Semestre -->
                                        <td class="celda-alumno texto-secundario">
                                    Semestre <xsl:value-of select="semestre"/>
                                        </td>

                                        <!-- Promedio -->
                                        <td class="celda-alumno promedio-alumno">
                                            <xsl:value-of select="format-number(promedio, '0.0')"/>
                                        </td>

                                        <!-- Lógica condicional para el Estatus -->
                                        <td class="celda-alumno">
                                            <xsl:choose>
                                                <xsl:when test="estatus = 'Activo'">
                                                    <span class="badge-estatus badge-activo">
                                                        <xsl:value-of select="estatus"/>
                                                    </span>
                                                </xsl:when>
                                                <xsl:when test="estatus = 'Egresado'">
                                                    <span class="badge-estatus badge-egresado">
                                                        <xsl:value-of select="estatus"/>
                                                    </span>
                                                </xsl:when>
                                                <xsl:otherwise>
                                                    <span class="badge-estatus badge-baja">
                                                        <xsl:value-of select="estatus"/>
                                                    </span>
                                                </xsl:otherwise>
                                            </xsl:choose>
                                        </td>

                                        <!-- Botón Eliminar -->
                                        <td class="celda-alumno texto-derecha">
                                            <button onclick="eliminarAlumno('{@id}')" class="boton boton-peligro boton-pequeno">
                                        Eliminar
                                            </button>
                                        </td>

                                    </tr>
                                </xsl:for-each>

                            </tbody>
                        </table>
                    </div>

                    <!-- MODAL NUEVO ALUMNO -->
                    <div id="modalNuevoAlumno" class="modal-overlay hidden">
                        <div class="modal-contenido">
                            <div class="modal-encabezado">
                                <h3 class="modal-titulo">Registrar Nuevo Alumno</h3>
                                <button onclick="cerrarModal()" class="boton-cerrar">&#215;</button>
                            </div>

                            <form id="formNuevoAlumno" onsubmit="guardarAlumno(event)">
                                <div class="formulario-grid formulario-dos-columnas espacio-inferior">
                                    <div>
                                        <label class="etiqueta-campo">ID del Nodo</label>
                                        <input type="text" name="id" placeholder="Ej. A006" required="required" class="campo-formulario"/>
                                    </div>
                                    <div>
                                        <label class="etiqueta-campo">Matrícula</label>
                                        <input type="text" name="matricula" placeholder="Ej. 20260006" required="required" class="campo-formulario"/>
                                    </div>
                                </div>
                                <div class="formulario-grid formulario-dos-columnas espacio-inferior">
                                    <div>
                                        <label class="etiqueta-campo">Nombre(s)</label>
                                        <input type="text" name="nombre" required="required" class="campo-formulario"/>
                                    </div>
                                    <div>
                                        <label class="etiqueta-campo">Apellidos</label>
                                        <input type="text" name="apellidos" required="required" class="campo-formulario"/>
                                    </div>
                                </div>
                                <div class="grupo-campo espacio-inferior">
                                    <label class="etiqueta-campo">Correo Electrónico</label>
                                    <input type="email" name="correo" required="required" class="campo-formulario"/>
                                </div>
                                <div class="formulario-grid formulario-cuatro-columnas espacio-inferior">
                                    <div class="columna-doble">
                                        <label class="etiqueta-campo">Carrera ID</label>
                                        <input type="text" name="carrera_id" placeholder="C001" required="required" class="campo-formulario"/>
                                    </div>
                                    <div>
                                        <label class="etiqueta-campo">Semestre</label>
                                        <input type="number" name="semestre" min="1" max="12" required="required" class="campo-formulario"/>
                                    </div>
                                    <div>
                                        <label class="etiqueta-campo">Promedio</label>
                                        <input type="number" step="0.1" name="promedio" required="required" class="campo-formulario"/>
                                    </div>
                                </div>
                                <div class="grupo-campo espacio-inferior-grande">
                                    <label class="etiqueta-campo">Estatus</label>
                                    <select name="estatus" class="campo-formulario">
                                        <option value="Activo">Activo</option>
                                        <option value="Egresado">Egresado</option>
                                        <option value="Baja">Baja</option>
                                    </select>
                                </div>
                                <div class="acciones-formulario">
                                    <button type="button" onclick="cerrarModal()" class="boton boton-secundario">Cancelar</button>
                                    <button type="submit" class="boton boton-exito">Guardar Alumno</button>
                                </div>
                            </form>
                        </div>
                    </div>
                </div>
            </body>
        </html>
    </xsl:template>
</xsl:stylesheet>