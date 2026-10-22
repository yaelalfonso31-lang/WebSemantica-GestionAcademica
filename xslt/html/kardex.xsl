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
                            <path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                        </svg>
                    </div>
                    <div>
                        <h1 class="page-header__title">Mi Kardex Académico</h1>
                        <p class="page-header__subtitle">
                            Historial oficial de materias y calificaciones cursadas
                        </p>
                    </div>
                </div>
                <span class="page-header__badge">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                    </svg>
                    Historial oficial
                </span>
            </div>

            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-card__icon">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"/>
                        </svg>
                    </div>
                    <div class="stat-card__body">
                        <span class="stat-card__label">Total Materias</span>
                        <span class="stat-card__value">
                            <xsl:value-of select="count(inscripciones/inscripcion)"/>
                        </span>
                    </div>
                </div>

                <div class="stat-card stat-card--success">
                    <div class="stat-card__icon">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                        </svg>
                    </div>
                    <div class="stat-card__body">
                        <span class="stat-card__label">Materias Aprobadas</span>
                        <span class="stat-card__value">
                            <xsl:value-of select="count(inscripciones/inscripcion[estatus='Aprobado'])"/>
                        </span>
                    </div>
                </div>

                <div class="stat-card stat-card--gold">
                    <div class="stat-card__icon">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
                        </svg>
                    </div>
                    <div class="stat-card__body">
                        <span class="stat-card__label">Promedio General</span>
                        <span class="stat-card__value">
                            <xsl:choose>
                                <xsl:when test="count(inscripciones/inscripcion[calificacion_final != '']) &gt; 0">
                                    <xsl:value-of select="format-number(sum(inscripciones/inscripcion[calificacion_final != '']/calificacion_final) div count(inscripciones/inscripcion[calificacion_final != '']), '0.0')"/>
                                </xsl:when>
                                <xsl:otherwise>0.0</xsl:otherwise>
                            </xsl:choose>
                        </span>
                    </div>
                </div>
            </div>

            <div class="table-card">
                <div class="table-card__header">
                    <h2 class="table-card__title">Desglose de Calificaciones</h2>
                    <span class="table-card__badge">
                        <xsl:value-of select="count(inscripciones/inscripcion)"/>
                        <xsl:text> registros</xsl:text>
                    </span>
                </div>

                <div class="table-scroll">
                    <table class="data-table kardex-table">
                        <thead>
                            <tr>
                                <th class="kardex-col-folio">Folio Ins.</th>
                                <th>Materia</th>
                                <th class="kardex-col-cred text-center">Créditos</th>
                                <th class="kardex-col-periodo">Periodo</th>
                                <th class="kardex-col-calif text-center">Calificación</th>
                                <th class="kardex-col-estatus text-center">Estatus</th>
                            </tr>
                        </thead>
                        <tbody>
                            <xsl:for-each select="inscripciones/inscripcion">
                                <xsl:sort select="periodo" order="descending"/>

                                <tr>
                                    <td class="kardex-col-folio">
                                        <span class="folio">
                                            <xsl:value-of select="@id"/>
                                        </span>
                                    </td>

                                    <td>
                                        <div class="cell-primary">
                                            <xsl:choose>
                                                <xsl:when test="materia_nombre != ''">
                                                    <xsl:value-of select="materia_nombre"/>
                                                </xsl:when>
                                                <xsl:otherwise>
                                                    <xsl:value-of select="materia_id"/>
                                                </xsl:otherwise>
                                            </xsl:choose>
                                        </div>
                                        <div class="cell-secondary">
                                            <span class="materia-code">
                                                <xsl:value-of select="materia_id"/>
                                            </span>
                                        </div>
                                    </td>

                                    <td class="kardex-col-cred text-center">
                                        <span class="creditos">
                                            <xsl:value-of select="creditos"/>
                                        </span>
                                    </td>

                                    <td class="kardex-col-periodo">
                                        <span class="periodo-chip">
                                            <xsl:value-of select="periodo"/>
                                        </span>
                                    </td>

                                    <td class="kardex-col-calif text-center">
                                        <xsl:choose>
                                            <xsl:when test="calificacion_final != ''">
                                                <span class="calificacion">
                                                    <xsl:value-of select="calificacion_final"/>
                                                </span>
                                            </xsl:when>
                                            <xsl:otherwise>
                                                <span class="calificacion calificacion--empty">—</span>
                                            </xsl:otherwise>
                                        </xsl:choose>
                                    </td>

                                    <td class="kardex-col-estatus text-center">
                                        <xsl:choose>
                                            <xsl:when test="estatus = 'Aprobado'">
                                                <span class="estatus-badge estatus-badge--aprobado">Aprobado</span>
                                            </xsl:when>
                                            <xsl:when test="estatus = 'Reprobado'">
                                                <span class="estatus-badge estatus-badge--reprobado">Reprobado</span>
                                            </xsl:when>
                                            <xsl:when test="estatus = 'Cursando'">
                                                <span class="estatus-badge estatus-badge--cursando">Cursando</span>
                                            </xsl:when>
                                            <xsl:otherwise>
                                                <span class="estatus-badge">
                                                    <xsl:value-of select="estatus"/>
                                                </span>
                                            </xsl:otherwise>
                                        </xsl:choose>
                                    </td>
                                </tr>
                            </xsl:for-each>

                            <xsl:if test="count(inscripciones/inscripcion) = 0">
                                <tr>
                                    <td colspan="6" class="empty-row">
                                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
                                            <path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                                        </svg>
                                        <p>Aún no tienes registros en tu historial académico.</p>
                                    </td>
                                </tr>
                            </xsl:if>
                        </tbody>
                    </table>
                </div>
            </div>

        </div>
    </xsl:template>
</xsl:stylesheet>