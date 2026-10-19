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
                            <path stroke-linecap="round" stroke-linejoin="round" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z"/>
                        </svg>
                    </div>
                    <div>
                        <h1 class="page-header__title">Módulo de Alumnos</h1>
                        <p class="page-header__subtitle">
                            EduSemantic · Sistema Web Semántico de Gestión Académica
                        </p>
                    </div>
                </div>
                <button type="button" onclick="abrirModal()" class="btn-app btn-app--primary">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4"/>
                    </svg>
                    Nuevo Alumno
                </button>
            </div>

            <!-- ============================
                 TARJETAS DE RESUMEN
                 ============================ -->
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-card__icon">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z"/>
                        </svg>
                    </div>
                    <div class="stat-card__body">
                        <span class="stat-card__label">Total de Alumnos</span>
                        <span class="stat-card__value">
                            <xsl:value-of select="count(alumnos/alumno)"/>
                        </span>
                    </div>
                </div>

                <div class="stat-card">
                    <div class="stat-card__icon">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
                        </svg>
                    </div>
                    <div class="stat-card__body">
                        <span class="stat-card__label">Promedio General</span>
                        <span class="stat-card__value">
                            <xsl:choose>
                                <xsl:when test="count(alumnos/alumno) &gt; 0">
                                    <xsl:value-of select="format-number(sum(alumnos/alumno/promedio) div count(alumnos/alumno), '0.0')"/>
                                </xsl:when>
                                <xsl:otherwise>0.0</xsl:otherwise>
                            </xsl:choose>
                        </span>
                    </div>
                </div>

                <div class="stat-card">
                    <div class="stat-card__icon">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                        </svg>
                    </div>
                    <div class="stat-card__body">
                        <span class="stat-card__label">Alumnos Activos</span>
                        <span class="stat-card__value">
                            <xsl:value-of select="count(alumnos/alumno[estatus='Activo'])"/>
                        </span>
                    </div>
                </div>
            </div>

            <!-- ============================
                 TABLA DE ALUMNOS
                 ============================ -->
            <div class="table-card">
                <div class="table-card__header">
                    <h2 class="table-card__title">Listado de Alumnos</h2>
                    <span class="table-card__badge">
                        <xsl:value-of select="count(alumnos/alumno)"/>
 registros
                    </span>
                </div>

                <div class="table-scroll">
                    <table class="data-table">
                        <thead>
                            <tr>
                                <th>Matrícula / ID</th>
                                <th>Alumno</th>
                                <th>Carrera</th>
                                <th>Semestre</th>
                                <th class="text-center">Promedio</th>
                                <th>Estatus</th>
                                <th class="text-right">Acciones</th>
                            </tr>
                        </thead>
                        <tbody>
                            <xsl:for-each select="alumnos/alumno">
                                <tr>
                                    <td>
                                        <div class="cell-primary">
                                            <xsl:value-of select="@matricula"/>
                                        </div>
                                        <div class="cell-secondary">
                                            ID: <xsl:value-of select="@id"/>
                                        </div>
                                    </td>
                                    <td>
                                        <div class="cell-primary">
                                            <xsl:value-of select="nombre"/>
                                            <xsl:text></xsl:text>
                                            <xsl:value-of select="apellidos"/>
                                        </div>
                                        <div class="cell-secondary">
                                            <xsl:value-of select="correo"/>
                                        </div>
                                    </td>
                                    <td>
                                        <span class="chip">
                                            <xsl:value-of select="carrera_id"/>
                                        </span>
                                    </td>
                                    <td class="cell-secondary">
                                        <xsl:value-of select="semestre"/>
                                        <xsl:text>º semestre</xsl:text>
                                    </td>
                                    <td class="text-center">
                                        <span class="promedio">
                                            <xsl:value-of select="format-number(promedio, '0.0')"/>
                                        </span>
                                    </td>
                                    <td>
                                        <xsl:choose>
                                            <xsl:when test="estatus = 'Activo'">
                                                <span class="status status--activo">
                                                    <xsl:value-of select="estatus"/>
                                                </span>
                                            </xsl:when>
                                            <xsl:when test="estatus = 'Egresado'">
                                                <span class="status status--egresado">
                                                    <xsl:value-of select="estatus"/>
                                                </span>
                                            </xsl:when>
                                            <xsl:otherwise>
                                                <span class="status status--baja">
                                                    <xsl:value-of select="estatus"/>
                                                </span>
                                            </xsl:otherwise>
                                        </xsl:choose>
                                    </td>
                                    <td class="text-right">
                                        <div class="actions">
                                            <button type="button" class="btn-action btn-action--edit" title="Editar alumno" onclick="abrirModalEditarAlumno('{@id}', '{@matricula}', '{nombre}', '{apellidos}', '{correo}', '{carrera_id}', '{semestre}', '{promedio}', '{estatus}')">
                                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                                                    <path stroke-linecap="round" stroke-linejoin="round" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
                                                </svg>
                                                Editar
                                            </button>
                                            <button type="button" class="btn-action btn-action--delete" title="Eliminar alumno" onclick="eliminarAlumno('{@id}')">
                                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                                                    <path stroke-linecap="round" stroke-linejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                                                </svg>
                                                Eliminar
                                            </button>
                                        </div>
                                    </td>
                                </tr>
                            </xsl:for-each>
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- ============================
                 MODAL NUEVO ALUMNO
                 ============================ -->
            <div id="modalNuevoAlumno" class="app-modal-overlay hidden">
                <div class="app-modal">
                    <div class="app-modal__header">
                        <div class="app-modal__header-icon">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z"/>
                            </svg>
                        </div>
                        <div class="app-modal__header-text">
                            <h3 class="app-modal__title">Registrar Nuevo Alumno</h3>
                            <p class="app-modal__subtitle">Completa los datos del estudiante</p>
                        </div>
                        <button type="button" onclick="cerrarModal()" class="app-modal__close" aria-label="Cerrar">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12"/>
                            </svg>
                        </button>
                    </div>

                    <form id="formNuevoAlumno" onsubmit="guardarAlumno(event)">
                        <div class="app-modal__body">
                            <div class="form-grid form-grid--2">
                                <div class="form-field">
                                    <label class="form-label">ID del Nodo</label>
                                    <input type="text" name="id" placeholder="Ej. A006" required="required" class="form-input"/>
                                </div>
                                <div class="form-field">
                                    <label class="form-label">Matrícula</label>
                                    <input type="text" name="matricula" placeholder="Ej. 20260006" required="required" class="form-input"/>
                                </div>
                            </div>

                            <div class="form-grid form-grid--2">
                                <div class="form-field">
                                    <label class="form-label">Nombre(s)</label>
                                    <input type="text" name="nombre" required="required" class="form-input"/>
                                </div>
                                <div class="form-field">
                                    <label class="form-label">Apellidos</label>
                                    <input type="text" name="apellidos" required="required" class="form-input"/>
                                </div>
                            </div>

                            <div class="form-field">
                                <label class="form-label">Correo Electrónico</label>
                                <input type="email" name="correo" required="required" class="form-input"/>
                            </div>

                            <div class="form-grid form-grid--3">
                                <div class="form-field">
                                    <label class="form-label">Carrera ID</label>
                                    <input type="text" name="carrera_id" placeholder="C001" required="required" class="form-input"/>
                                </div>
                                <div class="form-field">
                                    <label class="form-label">Semestre</label>
                                    <input type="number" name="semestre" min="1" max="12" required="required" class="form-input"/>
                                </div>
                                <div class="form-field">
                                    <label class="form-label">Promedio</label>
                                    <input type="number" step="0.1" name="promedio" required="required" class="form-input"/>
                                </div>
                            </div>

                            <div class="form-field">
                                <label class="form-label">Estatus</label>
                                <select name="estatus" class="form-input">
                                    <option value="Activo">Activo</option>
                                    <option value="Egresado">Egresado</option>
                                    <option value="Baja">Baja</option>
                                </select>
                            </div>
                        </div>

                        <div class="app-modal__footer">
                            <button type="button" onclick="cerrarModal()" class="btn-app btn-app--ghost">Cancelar</button>
                            <button type="submit" class="btn-app btn-app--primary">Guardar Alumno</button>
                        </div>
                    </form>
                </div>
            </div>

            <!-- ============================
                 MODAL EDITAR ALUMNO
                 ============================ -->
            <div class="app-modal-overlay hidden" id="modalEditarAlumno">
                <div class="app-modal">
                    <div class="app-modal__header">
                        <div class="app-modal__header-icon app-modal__header-icon--gold">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
                            </svg>
                        </div>
                        <div class="app-modal__header-text">
                            <h3 class="app-modal__title">Editar Alumno</h3>
                            <p class="app-modal__subtitle">Actualiza los datos del estudiante</p>
                        </div>
                        <button type="button" onclick="cerrarModalEditar()" class="app-modal__close" aria-label="Cerrar">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12"/>
                            </svg>
                        </button>
                    </div>

                    <form onsubmit="actualizarAlumno(event)">
                        <div class="app-modal__body">
                            <input type="hidden" id="edit_id" />

                            <div class="form-grid form-grid--2">
                                <div class="form-field">
                                    <label class="form-label">Matrícula</label>
                                    <input type="text" id="edit_matricula" class="form-input" required="required"/>
                                </div>
                                <div class="form-field">
                                    <label class="form-label">Correo Electrónico</label>
                                    <input type="email" id="edit_correo" class="form-input" required="required"/>
                                </div>
                            </div>

                            <div class="form-grid form-grid--2">
                                <div class="form-field">
                                    <label class="form-label">Nombre(s)</label>
                                    <input type="text" id="edit_nombre" class="form-input" required="required"/>
                                </div>
                                <div class="form-field">
                                    <label class="form-label">Apellidos</label>
                                    <input type="text" id="edit_apellidos" class="form-input" required="required"/>
                                </div>
                            </div>

                            <div class="form-grid form-grid--3">
                                <div class="form-field">
                                    <label class="form-label">Carrera ID</label>
                                    <input type="text" id="edit_carrera" class="form-input" required="required"/>
                                </div>
                                <div class="form-field">
                                    <label class="form-label">Semestre</label>
                                    <input type="number" id="edit_semestre" class="form-input" min="1" max="12" required="required"/>
                                </div>
                                <div class="form-field">
                                    <label class="form-label">Promedio</label>
                                    <input type="number" id="edit_promedio" step="0.1" class="form-input" required="required"/>
                                </div>
                            </div>

                            <div class="form-field">
                                <label class="form-label">Estatus</label>
                                <select id="edit_estatus" class="form-input">
                                    <option value="Activo">Activo</option>
                                    <option value="Egresado">Egresado</option>
                                    <option value="Baja">Baja</option>
                                </select>
                            </div>
                        </div>

                        <div class="app-modal__footer">
                            <button type="button" onclick="cerrarModalEditar()" class="btn-app btn-app--ghost">Cancelar</button>
                            <button type="submit" class="btn-app btn-app--primary">Guardar Cambios</button>
                        </div>
                    </form>
                </div>
            </div>

        </div>
    </xsl:template>
</xsl:stylesheet>