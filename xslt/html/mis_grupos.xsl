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
                        <h1 class="page-header__title">Mis Grupos Asignados</h1>
                        <p class="page-header__subtitle">
                            Periodo:
                            <xsl:choose>
                                <xsl:when test="normalize-space((mis_grupos/grupo/periodo)[1]) != ''">
                                    <xsl:value-of select="(mis_grupos/grupo/periodo)[1]"/>
                                </xsl:when>
                                <xsl:otherwise>No definido</xsl:otherwise>
                            </xsl:choose>
                        </p>
                    </div>
                </div>
                <span class="page-header__badge">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                    </svg>
                    <xsl:value-of select="count(mis_grupos/grupo)"/>
                    <xsl:text> grupos activos</xsl:text>
                </span>
            </div>

            <div class="grupos-grid">

                <xsl:for-each select="mis_grupos/grupo">
                    <article class="grupo-card">

                        <!-- Cabecera de la tarjeta -->
                        <div class="grupo-card__top">
                            <span class="grupo-card__materia-id">
                                <xsl:value-of select="materia_id"/>
                            </span>
                            <span class="grupo-card__grupo-id">
                                <xsl:value-of select="@id"/>
                            </span>
                        </div>

                        <!-- Título -->
                        <h3 class="grupo-card__title">
                            <xsl:value-of select="materia_nombre"/>
                        </h3>

                        <!-- Datos -->
                        <ul class="grupo-meta">

                            <li class="grupo-meta__item">
                                <span class="grupo-meta__icon">
                                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                                        <path stroke-linecap="round" stroke-linejoin="round" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
                                    </svg>
                                </span>
                                <div class="grupo-meta__body">
                                    <span class="grupo-meta__label">Días</span>
                                    <span class="grupo-meta__value">
                                        <xsl:choose>
                                            <xsl:when test="normalize-space(dia) != ''">
                                                <xsl:value-of select="dia"/>
                                            </xsl:when>
                                            <xsl:otherwise>Sin asignar</xsl:otherwise>
                                        </xsl:choose>
                                    </span>
                                </div>
                            </li>

                            <li class="grupo-meta__item">
                                <span class="grupo-meta__icon">
                                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                                        <path stroke-linecap="round" stroke-linejoin="round" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
                                    </svg>
                                </span>
                                <div class="grupo-meta__body">
                                    <span class="grupo-meta__label">Horario</span>
                                    <span class="grupo-meta__value">
                                        <xsl:value-of select="hora_inicio"/>
                                        <xsl:text> – </xsl:text>
                                        <xsl:value-of select="hora_fin"/>
                                    </span>
                                </div>
                            </li>

                            <li class="grupo-meta__item">
                                <span class="grupo-meta__icon">
                                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                                        <path stroke-linecap="round" stroke-linejoin="round" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"/>
                                    </svg>
                                </span>
                                <div class="grupo-meta__body">
                                    <span class="grupo-meta__label">Aula</span>
                                    <span class="grupo-meta__value">
                                        <xsl:choose>
                                            <xsl:when test="normalize-space(aula) != ''">
                                                <xsl:value-of select="aula"/>
                                            </xsl:when>
                                            <xsl:otherwise>Sin asignar</xsl:otherwise>
                                        </xsl:choose>
                                    </span>
                                </div>
                            </li>

                            <li class="grupo-meta__item">
                                <span class="grupo-meta__icon">
                                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                                        <path stroke-linecap="round" stroke-linejoin="round" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z"/>
                                    </svg>
                                </span>
                                <div class="grupo-meta__body">
                                    <span class="grupo-meta__label">Alumnos</span>
                                    <span class="grupo-meta__value">
                                        <xsl:value-of select="total_alumnos"/>
                                        <xsl:if test="pendientes &gt; 0">
                                            <span class="pendiente-badge">
                                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                                                    <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
                                                </svg>
                                                <xsl:value-of select="pendientes"/>
 sin calificar
                                            </span>
                                        </xsl:if>
                                    </span>
                                </div>
                            </li>

                        </ul>

                        <!-- Acción -->
                        <div class="grupo-card__footer">
                            <a href="/calificar?grupo={@id}" class="btn-app btn-app--primary btn-app--block">
                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
                                </svg>
                                Calificar Alumnos
                            </a>
                        </div>

                    </article>
                </xsl:for-each>

                <!-- Estado vacío -->
                <xsl:if test="count(mis_grupos/grupo) = 0">
                    <div class="grupos-empty">
                        <div class="grupos-empty__icon">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z"/>
                            </svg>
                        </div>
                        <h3 class="grupos-empty__title">Sin grupos asignados</h3>
                        <p class="grupos-empty__text">
                            No tienes grupos asignados en este periodo. Contacta a la coordinación académica si crees que esto es un error.
                        </p>
                    </div>
                </xsl:if>

            </div>
        </div>
    </xsl:template>
</xsl:stylesheet>