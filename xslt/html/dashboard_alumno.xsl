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
                            <path stroke-linecap="round" stroke-linejoin="round" d="M12 14l9-5-9-5-9 5 9 5z"/>
                            <path stroke-linecap="round" stroke-linejoin="round" d="M12 14l6.16-3.422A12.083 12.083 0 0112 21.5a12.083 12.083 0 01-6.16-10.922L12 14z"/>
                            <path stroke-linecap="round" stroke-linejoin="round" d="M12 14v7"/>
                        </svg>
                    </div>
                    <div class="welcome-banner__text">
                        <h1 class="welcome-banner__title">
                            ¡Bienvenido, <xsl:value-of select="$nombre_usuario"/>
!
                        </h1>
                        <p class="welcome-banner__subtitle">
                            Este es tu panel de estudiante. Desde aquí podrás consultar tu avance académico,
                            historial de calificaciones y los horarios de tus clases en el periodo actual.
                        </p>
                        <span class="welcome-banner__badge">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                            </svg>
                            Alumno Activo
                        </span>
                    </div>
                </div>
            </div>

            <div class="card-grid">

                <div class="module-card">
                    <div class="module-card__icon">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.8">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                        </svg>
                    </div>
                    <h3 class="module-card__title">Mi Kardex</h3>
                    <p class="module-card__desc">
                        Consulta tus calificaciones históricas y el estatus de tus materias aprobadas.
                    </p>
                    <a href="/kardex" class="btn-module btn-module--primary">
                        Ir al Kardex
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M13 7l5 5m0 0l-5 5m5-5H6"/>
                        </svg>
                    </a>
                </div>

                <div class="module-card">
                    <div class="module-card__icon">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.8">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
                        </svg>
                    </div>
                    <h3 class="module-card__title">Mi Horario</h3>
                    <p class="module-card__desc">
                        Revisa las clases, aulas y profesores que tienes asignados para este semestre.
                    </p>
                    <a href="/horarios" class="btn-module btn-module--secondary">
                        Ver Horario
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M13 7l5 5m0 0l-5 5m5-5H6"/>
                        </svg>
                    </a>
                </div>

            </div>
        </div>
    </xsl:template>
</xsl:stylesheet>