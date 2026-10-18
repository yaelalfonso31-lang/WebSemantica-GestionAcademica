<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

    <!-- Diseño general, navegación y estructura de la página -->
    <xsl:import href="layout.xsl"/>

    <xsl:template name="content">
        <div class="pagina-alumnos">
            <!-- Encabezado -->
            <header class="encabezado-modulo">
                <link rel="stylesheet" type="text/css" href="/static/css/alumnos.css"/>

                <div>
                    <h1 class="titulo-modulo">Módulo de Profesores</h1>
                    <p class="subtitulo-modulo">Sistema Web Semántico - Dashboard Administrativo</p>
                </div>
                <button type="button" class="boton boton-primario" onclick="abrirModalProfesor()">
                    + Nuevo Profesor
                </button>
            </header>

            <!-- Tabla de profesores -->
            <section class="tabla-contenedor">
                <table class="tabla-alumnos">
                    <thead class="tabla-encabezado">
                        <tr>
                            <th scope="col" class="celda-encabezado">ID</th>
                            <th scope="col" class="celda-encabezado">Profesor</th>
                            <th scope="col" class="celda-encabezado">Departamento</th>
                            <th scope="col" class="celda-encabezado">Materias impartidas</th>
                            <th scope="col" class="celda-encabezado texto-derecha">Acciones</th>
                        </tr>
                    </thead>

                    <tbody class="tabla-cuerpo">
                        <!-- Recorrer todos los profesores del XML -->
                        <xsl:for-each select="/profesores/profesor">
                            <tr class="fila-alumno">
                                <!-- Identificador -->
                                <td>
                                    <span class="matricula-alumno">
                                        <xsl:value-of select="@id"/>
                                    </span>
                                </td>

                                <!-- Datos del profesor -->
                                <td>
                                    <div class="nombre-alumno">
                                        <xsl:value-of select="nombre"/>
                                    </div>

                                    <div class="texto-secundario">
                                        <xsl:choose>
                                            <xsl:when test="normalize-space(especialidad) != ''">
                                                <xsl:value-of select="especialidad"/>
                                            </xsl:when>
                                            <xsl:otherwise>
                                                Sin especialidad registrada
                                            </xsl:otherwise>
                                        </xsl:choose>
                                    </div>

                                    <span class="correo-alumno">
                                        <xsl:value-of select="correo"/>
                                    </span>
                                </td>

                                <!-- Departamento -->
                                <td>
                                    <span class="etiqueta-carrera">
                                        <xsl:choose>
                                            <xsl:when test="normalize-space(departamento) != ''">
                                                <xsl:value-of select="departamento"/>
                                            </xsl:when>
                                            <xsl:otherwise>
                                                Sin departamento
                                            </xsl:otherwise>
                                        </xsl:choose>
                                    </span>
                                </td>

                                <!-- Materias impartidas -->
                                <td>
                                    <xsl:choose>
                                        <!-- Hay materias registradas -->
                                        <xsl:when test="materias_impartidas/materia">
                                            <ul>
                                                <xsl:for-each select="materias_impartidas/materia">
                                                    <li>
                                                        <span class="etiqueta-carrera">
                                                            <xsl:choose>
                                                                <xsl:when test="@codigo">
                                                                    <xsl:value-of select="@codigo"/>
                                                                </xsl:when>
                                                                <xsl:otherwise>
                                                                    Sin código
                                                                </xsl:otherwise>
                                                            </xsl:choose>
                                                        </span>

                                                        <span class="texto-secundario">
                                                            <xsl:text> </xsl:text>
                                                            <xsl:value-of select="normalize-space(.)"/>
                                                        </span>
                                                    </li>
                                                </xsl:for-each>
                                            </ul>

                                        </xsl:when>

                                        <!-- No hay materias -->
                                        <xsl:otherwise>
                                            <span class="texto-secundario">
                                                Sin materias asignadas
                                            </span>
                                        </xsl:otherwise>

                                    </xsl:choose>
                                </td>

                                <!-- Acciones -->
                                <td class="texto-derecha">
                                    <button type="button"
                                            class="boton boton-primario boton-pequeno"
                                            onclick="editarProfesor('{@id}')">
                                        Editar
                                    </button>
                                    <button type="button"
                                            class="boton boton-peligro boton-pequeno"
                                            onclick="eliminarProfesor('{@id}')">
                                        Eliminar
                                    </button>
                                </td>
                            </tr>
                        </xsl:for-each>

                        <!-- Mensaje cuando no existen profesores -->
                        <xsl:if test="not(/profesores/profesor)">
                            <tr>
                                <td colspan="5" style="text-align: center; padding: 30px;">
                                    <span class="texto-secundario">
                                        No hay profesores registrados.
                                    </span>
                                </td>
                            </tr>
                        </xsl:if>

                    </tbody>

                </table>

            </section>

            <!-- Modal para registrar y editar profesores -->
            <div id="modalProfesor" class="modal-overlay hidden">

                <div class="modal-contenido">

                    <!-- Encabezado del modal -->
                    <div class="modal-encabezado">
                        <h2 id="tituloModalProfesor" class="modal-titulo">
                            Registrar profesor
                        </h2>

                        <button type="button"
                                class="boton-cerrar"
                                aria-label="Cerrar formulario"
                                onclick="cerrarModalProfesor()">
                            &#215;
                        </button>
                    </div>

                    <!-- Formulario -->
                    <form id="formProfesor" onsubmit="guardarProfesor(event)">

                        <!-- Método HTTP: POST para registrar, PUT para editar -->
                        <input type="hidden"
                            id="metodoProfesor"
                            value="POST"/>

                        <div class="formulario-grid formulario-dos-columnas">

                            <!-- Identificador -->
                            <div>
                                <label for="idProfesor" class="etiqueta-campo">
                                    ID del profesor
                                </label>

                                <input
                                    type="text"
                                    id="idProfesor"
                                    name="id"
                                    class="campo-formulario"
                                    placeholder="P1001"
                                    pattern="[Pp][0-9]{{4}}"
                                    title="Ingresa P seguido de cuatro dígitos. Ejemplo: P1001."
                                    maxlength="5"
                                    required="required"
                                />
                            </div>

                            <!-- Nombre -->
                            <div>
                                <label for="nombreProfesor" class="etiqueta-campo">
                                    Nombre completo
                                </label>

                                <input type="text"
                                    id="nombreProfesor"
                                    name="nombre"
                                    class="campo-formulario"
                                    placeholder="Nombre del profesor"/>
                            </div>

                            <!-- Especialidad -->
                            <div>
                                <label for="especialidadProfesor" class="etiqueta-campo">
                                    Especialidad
                                </label>

                                <input type="text"
                                    id="especialidadProfesor"
                                    name="especialidad"
                                    class="campo-formulario"
                                    placeholder="Ej. Ingeniería de software"/>
                            </div>

                            <!-- Correo -->
                            <div>
                                <label for="correoProfesor" class="etiqueta-campo">
                                    Correo electrónico
                                </label>

                                <input type="email"
                                    id="correoProfesor"
                                    name="correo"
                                    class="campo-formulario"
                                    placeholder="profesor@edusemantic.edu"/>
                            </div>

                            <!-- Departamento -->
                            <div class="columna-doble">
                                <label for="departamentoProfesor"
                                    class="etiqueta-campo">
                                    Departamento
                                </label>

                                <input type="text"
                                    id="departamentoProfesor"
                                    name="departamento"
                                    class="campo-formulario"
                                    placeholder="Departamento académico"/>
                            </div>

                            <!-- Materias -->
                            <div class="columna-doble">
                                <label for="materiasProfesor"
                                    class="etiqueta-campo">
                                    Materias impartidas
                                </label>
         
                                <textarea
                                    id="materiasProfesor"
                                    name="materias"
                                    class="campo-formulario"
                                    rows="5"
                                    placeholder="CS201|Programación&#10;BD001|Bases de datos">
                                </textarea>

                                <small class="texto-secundario">
                                    Escribe una materia por línea con el formato CODIGO|Nombre.
                                    Ejemplo: CS201|Programación.
                                </small>
                            </div>

                        </div>

                        <!-- Botones -->
                        <div class="acciones-formulario">

                            <button type="button"
                                    class="boton boton-secundario"
                                    onclick="cerrarModalProfesor()">
                                Cancelar
                            </button>

                            <button type="submit"
                                    id="botonGuardarProfesor"
                                    class="boton boton-exito">
                                Guardar profesor
                            </button>

                        </div>

                    </form>

                </div>

            </div>

        </div>

    </xsl:template>

</xsl:stylesheet>
