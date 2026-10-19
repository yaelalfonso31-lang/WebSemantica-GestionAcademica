<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

    <xsl:import href="layout.xsl"/>

    <xsl:template name="content">
        <div class="container mt-4">
            <div class="mb-4">
                <h2 class="text-primary fw-bold mb-1">Mi Horario de Clases</h2>
                <p class="text-muted">Materias inscritas en el periodo actual.</p>
            </div>

            <div class="card shadow-sm border-0 border-top border-primary border-3">
                <div class="card-body p-0 table-responsive">
                    <table class="table table-hover table-striped mb-0 align-middle">
                        <thead class="table-dark">
                            <tr>
                                <th class="px-4">Grupo ID</th>
                                <th>Clave Materia</th>
                                <th>Días</th>
                                <th>Horario</th>
                                <th>Aula</th>
                            </tr>
                        </thead>
                        <tbody>
                            <!-- Iteramos sobre los grupos inyectados por Python -->
                            <xsl:for-each select="horario_alumno/grupo">
                                <tr>
                                    <td class="px-4">
                                        <span class="badge bg-primary rounded-pill">
                                            <xsl:value-of select="@id"/>
                                        </span>
                                    </td>
                                    <td class="fw-bold text-dark">
                                        <xsl:value-of select="materia_id"/>
                                    </td>
                                    <td>
                                        <xsl:value-of select="dia"/>
                                    </td>
                                    <td>
                                        <span class="text-muted">
                                            <xsl:value-of select="hora_inicio"/>
 -                                            <xsl:value-of select="hora_fin"/>
                                        </span>
                                    </td>
                                    <td>
                                        <span class="badge bg-light text-dark border">
                                            <xsl:value-of select="aula"/>
                                        </span>
                                    </td>
                                </tr>
                            </xsl:for-each>

                            <!-- Mensaje si no hay materias inscritas en este periodo -->
                            <xsl:if test="count(horario_alumno/grupo) = 0">
                                <tr>
                                    <td colspan="5" class="text-center py-5 text-muted">
                                        <div class="display-6 mb-3">📭</div>
                                        <em>No tienes materias inscritas con estatus "Cursando" en este momento.</em>
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