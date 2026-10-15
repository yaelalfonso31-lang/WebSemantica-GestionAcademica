<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

    <!-- Importamos el esqueleto principal -->
    <xsl:import href="layout.xsl" />

    <!-- Definimos el bloque de contenido -->
    <xsl:template name="content">
        <div class="tarjeta" style="max-width: 400px; margin: 2rem auto;">
            <h2>Acceso al Sistema</h2>

            <!-- Mostrar errores si el XML trae alguno (procesado desde auth_bp) -->
            <xsl:if test="login/errores/error">
                <div style="color: red; margin-bottom: 1rem;">
                    <xsl:for-each select="login/errores/error">
                        <p>&#9888; <xsl:value-of select="."/>
                        </p>
                    </xsl:for-each>
                </div>
            </xsl:if>

            <!-- Formulario HTML puro, sin Jinja -->
            <form action="/login" method="POST">
                <div style="margin-bottom: 1rem;">
                    <label for="username">Usuario:</label>
                    <br/>
                    <input type="text" id="username" name="username" required="required" style="width: 100%; padding: 0.5rem;"/>
                </div>
                <div style="margin-bottom: 1.5rem;">
                    <label for="password">Contraseña:</label>
                    <br/>
                    <input type="password" id="password" name="password" required="required" style="width: 100%; padding: 0.5rem;"/>
                </div>
                <button type="submit" style="width: 100%; padding: 0.7rem; background-color: #003b5c; color: white; border: none; cursor: pointer;">
                    Ingresar
                </button>
            </form>
        </div>
    </xsl:template>
</xsl:stylesheet>