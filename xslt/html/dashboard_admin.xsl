<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

    <xsl:import href="layout.xsl"/>

    <xsl:template name="content">
        <link rel="stylesheet" type="text/css" href="/static/css/dashboard.css"/>

        <div class="dashboard-wrapper">

            <div class="welcome-banner">
                <div class="welcome-banner__content">
                    <div class="welcome-banner__icon">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/>
                        </svg>
                    </div>
                    <div class="welcome-banner__text">
                        <h1 class="welcome-banner__title">Resumen General</h1>
                        <p class="welcome-banner__subtitle">
                            Bienvenido al sistema de gestión académica. Consulta las métricas globales de la institución.
                        </p>
                        <span class="welcome-banner__badge">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z"/>
                            </svg>
                            Nivel de acceso: <xsl:value-of select="$rol_usuario"/>
                        </span>
                    </div>
                </div>
            </div>

            <div class="metricas-container">
                <xsl:apply-templates select="dashboard/metricas/metrica" />
            </div>

        </div>
    </xsl:template>

    <xsl:template match="metrica">
        <div class="metrica-card">
            <p class="metrica-card__label">
                <xsl:value-of select="@nombre"/>
            </p>
            <p class="metrica-card__value">
                <xsl:value-of select="."/>
            </p>
        </div>
    </xsl:template>
</xsl:stylesheet>