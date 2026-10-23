<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:output method="html" encoding="UTF-8" indent="yes" />
    <xsl:param name="rol_usuario" select="'visitante'" />
    <xsl:param name="nombre_usuario" select="'Invitado'" />

    <xsl:template match="/">
        <html lang="es">
            <head>
                <meta charset="UTF-8" />
                <meta name="viewport" content="width=device-width, initial-scale=1.0" />
                <title>EduSemantic - Sistema Académico BUAP</title>

                <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet" />

                <link rel="stylesheet" href="/static/css/layout.css" />

                <link rel="stylesheet" href="/static/css/dashboard.css" />
                <link rel="stylesheet" href="/static/css/alumnos.css" />
                <link rel="stylesheet" href="/static/css/profesores.css" />
                <link rel="stylesheet" href="/static/css/materias.css" />
                <link rel="stylesheet" href="/static/css/consultas.css" />
                <link rel="stylesheet" href="/static/css/mis_grupos.css" />
                <link rel="stylesheet" href="/static/css/calificaciones.css" />
                <link rel="stylesheet" href="/static/css/horario.css" />
                <link rel="stylesheet" href="/static/css/grupos_admin.css" />
            </head>
            <body class="layout-body">

                <nav class="navbar navbar-expand-lg navbar-dark app-navbar ">
                    <div class="container">

                        <a class="navbar-brand app-navbar__brand" href="/dashboard">
                            <span class="app-navbar__logo">
                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M12 14l9-5-9-5-9 5 9 5z"/>
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M12 14l6.16-3.422A12.083 12.083 0 0112 21.5a12.083 12.083 0 01-6.16-10.922L12 14z"/>
                                </svg>
                            </span>
                            <span class="app-navbar__brand-text">
                                EduSemantic
                                <small>BUAP</small>
                            </span>
                        </a>

                        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                            <span class="navbar-toggler-icon"></span>
                        </button>

                        <div class="collapse navbar-collapse" id="navbarNav">
                            <ul class="navbar-nav me-auto app-navbar__links">
                                <li class="nav-item">
                                    <a class="nav-link" href="/dashboard">
                                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                                            <path stroke-linecap="round" stroke-linejoin="round" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/>
                                        </svg>
                                        Panel Principal
                                    </a>
                                </li>

                                <!-- VISTAS EXCLUSIVAS DEL ADMINISTRADOR -->
                                <xsl:if test="$rol_usuario = 'admin'">
                                    <li class="nav-item">
                                        <a class="nav-link" href="/alumnos">
                                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                                                <path stroke-linecap="round" stroke-linejoin="round" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z"/>
                                            </svg>
                                            Alumnos
                                        </a>
                                    </li>
                                    <li class="nav-item">
                                        <a class="nav-link" href="/profesores">
                                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                                                <path stroke-linecap="round" stroke-linejoin="round" d="M12 14l9-5-9-5-9 5 9 5z"/>
                                                <path stroke-linecap="round" stroke-linejoin="round" d="M12 14l6.16-3.422A12.083 12.083 0 0112 21.5a12.083 12.083 0 01-6.16-10.922L12 14z"/>
                                            </svg>
                                            Profesores
                                        </a>
                                    </li>
                                    <li class="nav-item">
                                        <a class="nav-link" href="/materias">
                                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                                                <path stroke-linecap="round" stroke-linejoin="round" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"/>
                                            </svg>
                                            Materias
                                        </a>
                                    </li>
                                    <li class="nav-item">
                                        <a class="nav-link" href="/grupos">
                                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                                                <path stroke-linecap="round" stroke-linejoin="round" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
                                            </svg>
                                            Grupos
                                        </a>
                                    </li>
                                    <li class="nav-item">
                                        <a class="nav-link app-navbar__link--accent" href="/consultas">
                                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                                                <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
                                            </svg>
                                            SPARQL
                                        </a>
                                    </li>
                                </xsl:if>

                                <!-- VISTAS EXCLUSIVAS DEL PROFESOR -->
                                <xsl:if test="$rol_usuario = 'profesor'">
                                    <li class="nav-item">
                                        <a class="nav-link" href="/mis_grupos">
                                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                                                <path stroke-linecap="round" stroke-linejoin="round" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z"/>
                                            </svg>
                                            Mis Grupos
                                        </a>
                                    </li>
                                    <li class="nav-item">
                                        <a class="nav-link" href="/calificar">
                                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                                                <path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                                            </svg>
                                            Calificaciones
                                        </a>
                                    </li>
                                    <li class="nav-item">
                                        <a class="nav-link" href="/horarios">
                                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                                                <path stroke-linecap="round" stroke-linejoin="round" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
                                            </svg>
                                            Mi Horario
                                        </a>
                                    </li>
                                </xsl:if>

                                <!-- VISTAS EXCLUSIVAS DEL ALUMNO -->
                                <xsl:if test="$rol_usuario = 'alumno'">
                                    <li class="nav-item">
                                        <a class="nav-link" href="/kardex">
                                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                                                <path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                                            </svg>
                                            Mi Kardex
                                        </a>
                                    </li>
                                    <li class="nav-item">
                                        <a class="nav-link" href="/horarios">
                                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                                                <path stroke-linecap="round" stroke-linejoin="round" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
                                            </svg>
                                            Mi Horario
                                        </a>
                                    </li>
                                </xsl:if>
                            </ul>

                            <!-- Zona de usuario -->
                            <ul class="navbar-nav app-navbar__user">
                                <xsl:choose>
                                    <xsl:when test="$rol_usuario != 'visitante'">
                                        <li class="nav-item app-navbar__user-item">
                                            <span class="app-navbar__avatar">
                                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                                                    <path stroke-linecap="round" stroke-linejoin="round" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
                                                </svg>
                                            </span>
                                            <div class="app-navbar__user-info">
                                                <span class="app-navbar__user-name">
                                                    <xsl:value-of select="$nombre_usuario"/>
                                                </span>
                                                <span class="app-navbar__user-role">
                                                    <xsl:value-of select="$rol_usuario"/>
                                                </span>
                                            </div>
                                        </li>
                                        <li class="nav-item">
                                            <a class="btn btn-sm app-navbar__logout" href="/logout">
                                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                                                    <path stroke-linecap="round" stroke-linejoin="round" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"/>
                                                </svg>
                                                Salir
                                            </a>
                                        </li>
                                    </xsl:when>
                                    <xsl:otherwise>
                                        <li class="nav-item">
                                            <a class="btn btn-sm app-navbar__login" href="/login">
                                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                                                    <path stroke-linecap="round" stroke-linejoin="round" d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1"/>
                                                </svg>
                                                Iniciar Sesión
                                            </a>
                                        </li>
                                    </xsl:otherwise>
                                </xsl:choose>
                            </ul>
                        </div>
                    </div>
                </nav>

                <!-- ============================
                     CONTENIDO PRINCIPAL
                     ============================ -->
                <main class="layout-main">
                    <xsl:call-template name="content" />
                </main>

                <!-- ============================
                     FOOTER
                     ============================ -->
                <footer class="app-footer">
                    <div class="container app-footer__inner">
                        <div class="app-footer__brand">
                            <strong>EduSemantic</strong> · Sistema Académico BUAP
                        </div>
                        <div class="app-footer__meta">
                            ©                            <xsl:value-of select="substring-before('2026-10-12', '-')"/>
 · Benemérita Universidad Autónoma de Puebla
                        </div>
                    </div>
                </footer>

                <!-- CDN de Bootstrap JS y script global -->
                <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
                <script src="/static/js/app.js"></script>
            </body>
        </html>
    </xsl:template>
</xsl:stylesheet>