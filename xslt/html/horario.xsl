<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:import href="layout.xsl"/>

    <!-- Sirve a alumnos (sus clases) y a profesores (los grupos que imparten) -->
    <xsl:template name="content">
        <xsl:variable name="rol" select="horario/@rol"/>
        <div class="alumnos-page">

            <div class="page-header">
                <div class="page-header__text">
                    <div class="page-header__icon">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
                        </svg>
                    </div>
                    <div>
                        <h1 class="page-header__title">Mi Horario Semanal</h1>
                        <p class="page-header__subtitle">
                            <xsl:choose>
                                <xsl:when test="$rol = 'profesor'">Clases que impartes en el periodo actual.</xsl:when>
                                <xsl:otherwise>Materias que cursas en el periodo actual.</xsl:otherwise>
                            </xsl:choose>
                        </p>
                    </div>
                </div>
                <span class="page-header__badge">
                    <xsl:value-of select="horario/resumen/clases"/>
                    <xsl:text> clases</xsl:text>
                </span>
            </div>

            <xsl:choose>
                <xsl:when test="count(horario/grupo) = 0">
                    <div class="horario-vacio">
                        <strong>Aún no tienes clases asignadas en este periodo.</strong>
                        <span>
                            <xsl:choose>
                                <xsl:when test="$rol = 'profesor'">Cuando el administrador te asigne grupos aparecerán aquí.</xsl:when>
                                <xsl:otherwise>Cuando te inscriban en un grupo aparecerá aquí.</xsl:otherwise>
                            </xsl:choose>
                        </span>
                    </div>
                </xsl:when>
                <xsl:otherwise>

                    <!-- Resumen -->
                    <div class="horario-resumen">
                        <div class="horario-resumen__item">
                            <span class="horario-resumen__label">Clases</span>
                            <span class="horario-resumen__value"><xsl:value-of select="horario/resumen/clases"/></span>
                        </div>
                        <div class="horario-resumen__item">
                            <span class="horario-resumen__label">Horas por semana</span>
                            <span class="horario-resumen__value"><xsl:value-of select="horario/resumen/horas"/></span>
                        </div>
                        <div class="horario-resumen__item">
                            <span class="horario-resumen__label">Créditos</span>
                            <span class="horario-resumen__value"><xsl:value-of select="horario/resumen/creditos"/></span>
                        </div>
                    </div>

                    <!-- Cuadrícula semanal -->
                    <div class="semana-wrap">
                        <table class="semana">
                            <thead>
                                <tr>
                                    <th class="semana__hora"></th>
                                    <xsl:for-each select="horario/semana/dia">
                                        <th><xsl:value-of select="."/></th>
                                    </xsl:for-each>
                                </tr>
                            </thead>
                            <tbody>
                                <xsl:for-each select="horario/semana/franja">
                                    <tr>
                                        <th class="semana__hora"><xsl:value-of select="@hora"/></th>
                                        <xsl:for-each select="celda">
                                            <xsl:choose>
                                                <xsl:when test="@tipo = 'clase'">
                                                    <td rowspan="{@filas}" class="semana__clase semana__c{@color}">
                                                        <xsl:if test="@choque = '1'">
                                                            <xsl:attribute name="class">semana__clase semana__c<xsl:value-of select="@color"/> semana__clase--choque</xsl:attribute>
                                                        </xsl:if>
                                                        <span class="semana__materia"><xsl:value-of select="@materia_nombre"/></span>
                                                        <span class="semana__linea"><xsl:value-of select="@inicio"/> – <xsl:value-of select="@fin"/></span>
                                                        <span class="semana__linea"><xsl:value-of select="@grupo"/> · <xsl:value-of select="@aula"/></span>
                                                        <xsl:choose>
                                                            <xsl:when test="$rol = 'profesor'">
                                                                <span class="semana__linea"><xsl:value-of select="@alumnos"/><xsl:choose><xsl:when test="@alumnos = 1"> alumno</xsl:when><xsl:otherwise> alumnos</xsl:otherwise></xsl:choose></span>
                                                            </xsl:when>
                                                            <xsl:otherwise>
                                                                <span class="semana__linea"><xsl:value-of select="@profesor_nombre"/></span>
                                                            </xsl:otherwise>
                                                        </xsl:choose>
                                                        <xsl:if test="@choque = '1'">
                                                            <span class="semana__aviso">Choque de horario</span>
                                                        </xsl:if>
                                                    </td>
                                                </xsl:when>
                                                <xsl:otherwise>
                                                    <td class="semana__vacia"></td>
                                                </xsl:otherwise>
                                            </xsl:choose>
                                        </xsl:for-each>
                                    </tr>
                                </xsl:for-each>
                            </tbody>
                        </table>
                    </div>

                    <!-- Detalle en lista -->
                    <h2 class="horario-subtitulo">Detalle de clases</h2>
                    <div class="table-responsive horario-detalle">
                        <table class="table table-hover mb-0 align-middle">
                            <thead>
                                <tr>
                                    <th>Grupo</th>
                                    <th>Materia</th>
                                    <th>
                                        <xsl:choose>
                                            <xsl:when test="$rol = 'profesor'">Alumnos</xsl:when>
                                            <xsl:otherwise>Profesor</xsl:otherwise>
                                        </xsl:choose>
                                    </th>
                                    <th>Días</th>
                                    <th>Horario</th>
                                    <th>Aula</th>
                                    <xsl:if test="$rol = 'profesor'"><th></th></xsl:if>
                                </tr>
                            </thead>
                            <tbody>
                                <xsl:for-each select="horario/grupo">
                                    <tr>
                                        <td><span class="horario-chip"><xsl:value-of select="@id"/></span></td>
                                        <td>
                                            <strong><xsl:value-of select="materia_nombre"/></strong>
                                            <div class="small text-muted"><xsl:value-of select="materia_id"/> · <xsl:value-of select="creditos"/> créditos</div>
                                        </td>
                                        <td>
                                            <xsl:choose>
                                                <xsl:when test="$rol = 'profesor'"><xsl:value-of select="alumnos"/></xsl:when>
                                                <xsl:otherwise><xsl:value-of select="profesor_nombre"/></xsl:otherwise>
                                            </xsl:choose>
                                        </td>
                                        <td><xsl:value-of select="dia"/></td>
                                        <td><xsl:value-of select="hora_inicio"/> – <xsl:value-of select="hora_fin"/></td>
                                        <td><xsl:value-of select="aula"/></td>
                                        <xsl:if test="$rol = 'profesor'">
                                            <td class="text-end"><a class="btn btn-sm btn-outline-primary" href="/calificar?grupo={@id}">Calificar</a></td>
                                        </xsl:if>
                                    </tr>
                                </xsl:for-each>
                            </tbody>
                        </table>
                    </div>
                </xsl:otherwise>
            </xsl:choose>
        </div>
    </xsl:template>
</xsl:stylesheet>
