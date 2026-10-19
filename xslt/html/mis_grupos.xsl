<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

    <xsl:import href="layout.xsl"/>

    <xsl:template name="content">
        <div class="container mt-4">
            <div class="d-flex justify-content-between align-items-center mb-4">
                <div>
                    <h2 class="text-warning fw-bold text-dark mb-1">Mis Grupos Asignados</h2>
                    <p class="text-muted">Ciclo Escolar: Otoño 2026</p>
                </div>
            </div>

            <div class="row">
                <xsl:for-each select="mis_grupos/grupo">
                    <div class="col-md-6 col-lg-4 mb-4">
                        <div class="card shadow-sm h-100 border-0 border-top border-warning border-3">
                            <div class="card-body">
                                <div class="d-flex justify-content-between align-items-start mb-2">
                                    <span class="badge bg-dark">
                                        <xsl:value-of select="materia_id"/>
                                    </span>
                                    <span class="badge bg-light text-dark border">
                                        <xsl:value-of select="@id"/>
                                    </span>
                                </div>

                                <h5 class="card-title text-dark fw-bold mt-3 mb-3">
                                    <!-- Aquí idealmente haríamos un cruce con materias.xml para mostrar el nombre, 
                                         pero por ahora mostramos la clave resaltada -->
                                    Materia:                                    <xsl:value-of select="materia_id"/>
                                </h5>

                                <ul class="list-unstyled text-muted mb-4">
                                    <li class="mb-2">
                                        <strong>📅 Días:</strong>
                                        <xsl:value-of select="dia"/>
                                    </li>
                                    <li class="mb-2">
                                        <strong>⏰ Horario:</strong>
                                        <xsl:value-of select="hora_inicio"/>
 -                                        <xsl:value-of select="hora_fin"/>
                                    </li>
                                    <li class="mb-2">
                                        <strong>🏫 Aula:</strong>
                                        <xsl:value-of select="aula"/>
                                    </li>
                                </ul>

                                <div class="d-grid gap-2">
                                    <!-- Este botón nos llevará al módulo de calificaciones en el siguiente paso -->
                                    <a href="/calificar?grupo={@id}&amp;materia={materia_id}" class="btn btn-outline-warning text-dark fw-bold">
                                        📝 Calificar Alumnos
                                    </a>
                                </div>
                            </div>
                        </div>
                    </div>
                </xsl:for-each>

                <!-- Si el profesor no tiene grupos asignados -->
                <xsl:if test="count(mis_grupos/grupo) = 0">
                    <div class="col-12 text-center py-5">
                        <h4 class="text-muted">No tienes grupos asignados en este periodo.</h4>
                    </div>
                </xsl:if>
            </div>
        </div>
    </xsl:template>
</xsl:stylesheet>