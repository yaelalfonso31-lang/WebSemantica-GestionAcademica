<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <!-- Importar la navegación y estructura base -->
    <xsl:import href="layout.xsl"/>

    <!-- Definir el contenido que se inyectará en el 'main' del layout -->
    <xsl:template name="content">
        <h1>Resumen General</h1>
        <p>Bienvenido al sistema. Tu nivel de acceso es: <strong>
            <xsl:value-of select="$rol_usuario"/>
        </strong>.
    </p>

    <!-- Procesar los datos que vengan en el XML dinámico del dashboard -->
    <div class="metricas-container">
        <xsl:apply-templates select="dashboard/metricas/metrica" />
    </div>
</xsl:template>

<xsl:template match="metrica">
    <div class="tarjeta">
        <h3>
            <xsl:value-of select="@nombre"/>
        </h3>
        <p>
            <xsl:value-of select="."/>
        </p>
    </div>
</xsl:template>
</xsl:stylesheet>