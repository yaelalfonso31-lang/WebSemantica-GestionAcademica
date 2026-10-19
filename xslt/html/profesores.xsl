<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

    <xsl:import href="layout.xsl"/>

    <xsl:template name="content">

        <div class="alumnos-page">


            <div class="page-header">
                <div class="page-header__text">
                    <div class="page-header__icon">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M12 14l9-5-9-5-9 5 9 5z"/>
                            <path stroke-linecap="round" stroke-linejoin="round" d="M12 14l6.16-3.422A12.083 12.083 0 0112 21.5a12.083 12.083 0 01-6.16-10.922L12 14z"/>
                        </svg>
                    </div>
                    <div>
                        <h1 class="page-header__title">Módulo de Profesores</h1>
                        <p class="page-header__subtitle">
                            Sistema Web Semántico · Dashboard Administrativo
                        </p>
                    </div>
                </div>
                <button type="button" onclick="abrirModalProfesor()" class="btn-app btn-app--primary">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4"/>
                    </svg>
                    Nuevo Profesor
                </button>
            </div>

            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-card__icon">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z"/>
                        </svg>
                    </div>
                    <div class="stat-card__body">
                        <span class="stat-card__label">Total de Profesores</span>
                        <span class="stat-card__value">
                            <xsl:value-of select="count(/profesores/profesor)"/>
                        </span>
                    </div>
                </div>

                <div class="stat-card">
                    <div class="stat-card__icon">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"/>
                        </svg>
                    </div>
                    <div class="stat-card__body">
                        <span class="stat-card__label">Departamentos</span>
                        <span class="stat-card__value">
                            <xsl:value-of select="count(//departamento[normalize-space(.) != ''])"/>
                        </span>
                    </div>
                </div>

                <div class="stat-card">
                    <div class="stat-card__icon">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"/>
                        </svg>
                    </div>
                    <div class="stat-card__body">
                        <span class="stat-card__label">Materias Impartidas</span>
                        <span class="stat-card__value">
                            <xsl:value-of select="count(//materias_impartidas/materia)"/>
                        </span>
                    </div>
                </div>
            </div>

            <!-- ============================
                 TABLA DE PROFESORES
                 ============================ -->
            <div class="table-card">
                <div class="table-card__header">
                    <h2 class="table-card__title">Listado de Profesores</h2>
                    <span class="table-card__badge">
                        <xsl:value-of select="count(/profesores/profesor)"/>
 registros
                    </span>
                </div>

                <div class="table-scroll">
                    <table class="data-table">
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Profesor</th>
                                <th>Departamento</th>
                                <th>Materias Impartidas</th>
                                <th class="text-right">Acciones</th>
                            </tr>
                        </thead>
                        <tbody>
                            <xsl:for-each select="/profesores/profesor">
                                <tr>
                                    <!-- ID -->
                                    <td>
                                        <span class="chip">
                                            <xsl:value-of select="@id"/>
                                        </span>
                                    </td>

                                    <!-- Profesor -->
                                    <td>
                                        <div class="cell-primary">
                                            <xsl:value-of select="nombre"/>
                                        </div>
                                        <div class="cell-secondary">
                                            <xsl:choose>
                                                <xsl:when test="normalize-space(especialidad) != ''">
                                                    <xsl:value-of select="especialidad"/>
                                                </xsl:when>
                                                <xsl:otherwise>Sin especialidad registrada</xsl:otherwise>
                                            </xsl:choose>
                                        </div>
                                        <div class="cell-secondary">
                                            <xsl:value-of select="correo"/>
                                        </div>
                                    </td>

                                    <!-- Departamento -->
                                    <td>
                                        <xsl:choose>
                                            <xsl:when test="normalize-space(departamento) != ''">
                                                <span class="chip">
                                                    <xsl:value-of select="departamento"/>
                                                </span>
                                            </xsl:when>
                                            <xsl:otherwise>
                                                <span class="cell-secondary">Sin departamento</span>
                                            </xsl:otherwise>
                                        </xsl:choose>
                                    </td>

                                    <!-- Materias impartidas -->
                                    <td>
                                        <xsl:choose>
                                            <xsl:when test="materias_impartidas/materia">
                                                <ul class="materias-list">
                                                    <xsl:for-each select="materias_impartidas/materia">
                                                        <li class="materias-list__item">
                                                            <span class="materias-list__code">
                                                                <xsl:choose>
                                                                    <xsl:when test="@codigo">
                                                                        <xsl:value-of select="@codigo"/>
                                                                    </xsl:when>
                                                                    <xsl:otherwise>—</xsl:otherwise>
                                                                </xsl:choose>
                                                            </span>
                                                            <span class="materias-list__name">
                                                                <xsl:value-of select="normalize-space(.)"/>
                                                            </span>
                                                        </li>
                                                    </xsl:for-each>
                                                </ul>
                                            </xsl:when>
                                            <xsl:otherwise>
                                                <span class="cell-secondary">Sin materias asignadas</span>
                                            </xsl:otherwise>
                                        </xsl:choose>
                                    </td>

                                    <!-- Acciones -->
                                    <td class="text-right">
                                        <div class="actions">
                                            <button type="button" class="btn-action btn-action--edit" title="Editar profesor" onclick="editarProfesor('{@id}')">
                                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                                                    <path stroke-linecap="round" stroke-linejoin="round" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
                                                </svg>
                                                Editar
                                            </button>
                                            <button type="button" class="btn-action btn-action--delete" title="Eliminar profesor" onclick="eliminarProfesor('{@id}')">
                                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                                                    <path stroke-linecap="round" stroke-linejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                                                </svg>
                                                Eliminar
                                            </button>
                                        </div>
                                    </td>
                                </tr>
                            </xsl:for-each>

                            <!-- Mensaje cuando no existen profesores -->
                            <xsl:if test="not(/profesores/profesor)">
                                <tr>
                                    <td colspan="5" class="empty-row">
                                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
                                            <path stroke-linecap="round" stroke-linejoin="round" d="M12 14l9-5-9-5-9 5 9 5z"/>
                                            <path stroke-linecap="round" stroke-linejoin="round" d="M12 14l6.16-3.422A12.083 12.083 0 0112 21.5a12.083 12.083 0 01-6.16-10.922L12 14z"/>
                                        </svg>
                                        <p>No hay profesores registrados.</p>
                                        <button type="button" onclick="abrirModalProfesor()" class="btn-app btn-app--primary">
                                            Registrar el primero
                                        </button>
                                    </td>
                                </tr>
                            </xsl:if>
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- ============================
                 MODAL PROFESOR (nuevo / editar)
                 ============================ -->
            <div id="modalProfesor" class="app-modal-overlay hidden">
                <div class="app-modal">
                    <div class="app-modal__header">
                        <div class="app-modal__header-icon">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M12 14l9-5-9-5-9 5 9 5z"/>
                                <path stroke-linecap="round" stroke-linejoin="round" d="M12 14l6.16-3.422A12.083 12.083 0 0112 21.5a12.083 12.083 0 01-6.16-10.922L12 14z"/>
                            </svg>
                        </div>
                        <div class="app-modal__header-text">
                            <h3 id="tituloModalProfesor" class="app-modal__title">Registrar Profesor</h3>
                            <p class="app-modal__subtitle">Completa los datos del docente</p>
                        </div>
                        <button type="button" class="app-modal__close" onclick="cerrarModalProfesor()" aria-label="Cerrar">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12"/>
                            </svg>
                        </button>
                    </div>

                    <form id="formProfesor" onsubmit="guardarProfesor(event)">
                        <input type="hidden" id="metodoProfesor" value="POST"/>

                        <div class="app-modal__body">

                            <div class="form-grid form-grid--2">
                                <div class="form-field">
                                    <label for="idProfesor" class="form-label">ID del Profesor</label>
                                    <input type="text" id="idProfesor" name="id" class="form-input" placeholder="P1001" pattern="[Pp][0-9]{{4}}" title="Ingresa P seguido de cuatro dígitos. Ejemplo: P1001." maxlength="5" required="required"/>
                                </div>
                                <div class="form-field">
                                    <label for="nombreProfesor" class="form-label">Nombre Completo</label>
                                    <input type="text" id="nombreProfesor" name="nombre" class="form-input" placeholder="Nombre del profesor" required="required"/>
                                </div>
                            </div>

                            <div class="form-grid form-grid--2">
                                <div class="form-field">
                                    <label for="especialidadProfesor" class="form-label">Especialidad</label>
                                    <input type="text" id="especialidadProfesor" name="especialidad" class="form-input" placeholder="Ej. Ingeniería de software"/>
                                </div>
                                <div class="form-field">
                                    <label for="correoProfesor" class="form-label">Correo Electrónico</label>
                                    <input type="email" id="correoProfesor" name="correo" class="form-input" placeholder="profesor@edusemantic.edu" required="required"/>
                                </div>
                            </div>

                            <div class="form-field">
                                <label for="departamentoProfesor" class="form-label">Departamento</label>
                                <input type="text" id="departamentoProfesor" name="departamento" class="form-input" placeholder="Departamento académico"/>
                            </div>

                            <div class="form-field">
                                <label for="materiasProfesor" class="form-label">Materias Impartidas</label>
                                <textarea id="materiasProfesor" name="materias" class="form-input form-textarea" rows="5" placeholder="CS201|Programación&#10;BD001|Bases de datos"></textarea>
                                <small class="form-help">
                                    Escribe una materia por línea con el formato <strong>CODIGO|Nombre</strong>.
                                    Ejemplo: <code>CS201|Programación</code>.
                                </small>
                            </div>

                        </div>

                        <div class="app-modal__footer">
                            <button type="button" class="btn-app btn-app--ghost" onclick="cerrarModalProfesor()">
                                Cancelar
                            </button>
                            <button type="submit" id="botonGuardarProfesor" class="btn-app btn-app--primary">
                                Guardar Profesor
                            </button>
                        </div>
                    </form>
                </div>
            </div>

        </div>
    </xsl:template>
</xsl:stylesheet>