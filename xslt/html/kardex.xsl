<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

    <xsl:import href="layout.xsl"/>

    <xsl:template name="content">
        <!-- CSS Específico del Kardex -->
        <link rel="stylesheet" href="/static/css/kardex.css" />

        <div class="row mb-4 align-items-center">
            <div class="col-md-8">
                <h1 class="text-primary fw-bold">Mi Kardex Académico</h1>
                <p class="text-secondary mb-0">Historial oficial de materias y calificaciones cursadas.</p>
            </div>
        </div>

        <!-- Tarjetas de Estadísticas usando Grid de Bootstrap -->
        <div class="row mb-4">
            <div class="col-md-4 mb-3">
                <div class="card shadow-sm border-0 border-start border-primary border-4 h-100">
                    <div class="card-body">
                        <h6 class="text-muted text-uppercase mb-1">Total Materias</h6>
                        <h3 class="fw-bold mb-0 text-dark">
                            <xsl:value-of select="count(inscripciones/inscripcion)"/>
                        </h3>
                    </div>
                </div>
            </div>
            <div class="col-md-4 mb-3">
                <div class="card shadow-sm border-0 border-start border-success border-4 h-100">
                    <div class="card-body">
                        <h6 class="text-muted text-uppercase mb-1">Materias Aprobadas</h6>
                        <h3 class="fw-bold mb-0 text-success">
                            <xsl:value-of select="count(inscripciones/inscripcion[estatus='Aprobado'])"/>
                        </h3>
                    </div>
                </div>
            </div>
            <div class="col-md-4 mb-3">
                <div class="card shadow-sm border-0 border-start border-info border-4 h-100">
                    <div class="card-body">
                        <h6 class="text-muted text-uppercase mb-1">Promedio General</h6>
                        <h3 class="fw-bold mb-0 text-info">
                            <!-- XPath para calcular el promedio dinámicamente ignorando las materias 'Cursando' -->
                            <xsl:choose>
                                <xsl:when test="count(inscripciones/inscripcion[calificacion_final != '']) &gt; 0">
                                    <xsl:value-of select="format-number(sum(inscripciones/inscripcion[calificacion_final != '']/calificacion_final) div count(inscripciones/inscripcion[calificacion_final != '']), '0.0')"/>
                                </xsl:when>
                                <xsl:otherwise>0.0</xsl:otherwise>
                            </xsl:choose>
                        </h3>
                    </div>
                </div>
            </div>
        </div>

        <!-- Tabla del Historial -->
        <div class="card shadow-sm border-0">
            <div class="card-header bg-white py-3">
                <h5 class="mb-0 fw-bold">Desglose de Calificaciones</h5>
            </div>
            <div class="card-body p-0 table-responsive">
                <table class="table table-hover table-striped mb-0 align-middle">
                    <thead class="table-dark">
                        <tr>
                            <th class="px-4">Folio Ins.</th>
                            <th>Clave Materia</th>
                            <th>Periodo</th>
                            <th class="text-center">Calificación</th>
                            <th class="text-center">Estatus</th>
                        </tr>
                    </thead>
                    <tbody>
                        <!-- Ordenamos las inscripciones por periodo de manera descendente -->
                        <xsl:for-each select="inscripciones/inscripcion">
                            <xsl:sort select="periodo" order="descending"/>

                            <tr>
                                <td class="px-4 text-muted badge-mono">
                                    <xsl:value-of select="@id"/>
                                </td>
                                <td>
                                    <span class="badge bg-secondary badge-mono">
                                        <xsl:value-of select="materia_id"/>
                                    </span>
                                </td>
                                <td>
                                    <xsl:value-of select="periodo"/>
                                </td>

                                <td class="text-center fw-bold">
                                    <xsl:choose>
                                        <xsl:when test="calificacion_final != ''">
                                            <xsl:value-of select="calificacion_final"/>
                                        </xsl:when>
                                        <xsl:otherwise>
                                            <span class="text-muted">-</span>
                                        </xsl:otherwise>
                                    </xsl:choose>
                                </td>

                                <td class="text-center">
                                    <!-- Lógica para aplicar colores a los badges de Bootstrap -->
                                    <xsl:choose>
                                        <xsl:when test="estatus = 'Aprobado'">
                                            <span class="badge bg-success px-3 py-2">Aprobado</span>
                                        </xsl:when>
                                        <xsl:when test="estatus = 'Reprobado'">
                                            <span class="badge bg-danger px-3 py-2">Reprobado</span>
                                        </xsl:when>
                                        <xsl:when test="estatus = 'Cursando'">
                                            <span class="badge bg-warning text-dark px-3 py-2">Cursando</span>
                                        </xsl:when>
                                        <xsl:otherwise>
                                            <span class="badge bg-secondary px-3 py-2">
                                                <xsl:value-of select="estatus"/>
                                            </span>
                                        </xsl:otherwise>
                                    </xsl:choose>
                                </td>
                            </tr>
                        </xsl:for-each>

                        <!-- Si el alumno es nuevo y no tiene materias -->
                        <xsl:if test="count(inscripciones/inscripcion) = 0">
                            <tr>
                                <td colspan="5" class="text-center py-5 text-muted">
                                    <em>Aún no tienes registros en tu historial académico.</em>
                                </td>
                            </tr>
                        </xsl:if>
                    </tbody>
                </table>
            </div>
        </div>

    </xsl:template>
</xsl:stylesheet>