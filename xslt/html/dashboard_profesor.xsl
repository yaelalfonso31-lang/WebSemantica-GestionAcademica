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
                            Portal Docente
                        </h1>
                        <p class="welcome-banner__subtitle">
                            Bienvenido, Profesor <xsl:value-of select="$nombre_usuario"/>
.
                            Gestiona tus grupos asignados y captura las calificaciones de tus alumnos.
                        </p>
                        <span class="welcome-banner__badge">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                            </svg>
                            Acceso Docente
                        </span>
                    </div>
                </div>
            </div>

            <div class="card-grid">
                <div class="module-card">
                    <div class="module-card__icon">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.8">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"/>
                        </svg>
                    </div>
                    <h3 class="module-card__title">Mis Grupos</h3>
                    <p class="module-card__desc">
                        Revisa la lista de alumnos inscritos en las materias que impartes.
                    </p>
                    <a href="/mis_grupos" class="btn-module btn-module--primary">
                        Ver Grupos
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M13 7l5 5m0 0l-5 5m5-5H6"/>
                        </svg>
                    </a>
                </div>

                <!-- Evaluaciones -->
                <div class="module-card">
                    <div class="module-card__icon">
                        <!-- Icono: libreta / editar -->
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.8">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                        </svg>
                    </div>
                    <h3 class="module-card__title">Evaluaciones</h3>
                    <p class="module-card__desc">
                        Captura las calificaciones ordinarias y extraordinarias del periodo.
                    </p>
                    <a href="/calificar" class="btn-module btn-module--secondary">
                        Capturar Notas
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M13 7l5 5m0 0l-5 5m5-5H6"/>
                        </svg>
                    </a>
                </div>

            </div>
        </div>
    </xsl:template>
</xsl:stylesheet>