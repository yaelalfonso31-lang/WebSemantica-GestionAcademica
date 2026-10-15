<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:output method="html" encoding="UTF-8" indent="yes" />

    <!-- Parámetros globales inyectados desde Python -->
    <xsl:param name="rol_usuario" select="'visitante'" />
    <xsl:param name="nombre_usuario" select="'Invitado'" />

    <xsl:template match="/">
        <html lang="es">
            <head>
                <meta charset="UTF-8" />
                <title>Sistema Semántico Académico</title>
                <!-- Aquí podrías enlazar tu CSS cuando lo tengas -->
                <link rel="stylesheet" href="/static/css/layout.css" />

            </head>
            <body>
                <nav>
                    <a href="/dashboard">Panel de Control</a>

                    <!-- Menú dinámico basado en el rol -->
                    <xsl:if test="$rol_usuario = 'admin'">
                        <a href="/alumnos">Alumnos</a>
                        <a href="/profesores">Profesores</a>
                        <a href="/materias">Materias</a>
                    </xsl:if>
                    <xsl:if test="$rol_usuario = 'alumno'">
                        <a href="/kardex">Mi Kardex</a>
                        <a href="/horarios">Mi Horario</a>
                    </xsl:if>

                    <xsl:choose>
                        <xsl:when test="$rol_usuario != 'visitante'">
                            <a href="/logout" style="float:right;">Cerrar Sesión (<xsl:value-of select="$nombre_usuario"/>
)</a>
                        </xsl:when>
                        <xsl:otherwise>
                            <a href="/login" style="float:right;">Iniciar Sesión</a>
                        </xsl:otherwise>
                    </xsl:choose>
                </nav>
                <main>
                    <!-- Las demás páginas inyectarán su contenido aquí -->
                    <xsl:call-template name="content" />
                </main>
                <script src="/static/js/app.js"></script>
            </body>
        </html>
    </xsl:template>
</xsl:stylesheet>