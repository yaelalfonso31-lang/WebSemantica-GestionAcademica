<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:import href="layout.xsl"/>
    <xsl:param name="codigo" select="'500'"/>
    <xsl:param name="titulo" select="'Error'"/>
    <xsl:param name="detalle" select="''"/>

    <xsl:template name="content">
        <div class="container py-5 text-center">
            <p class="display-1 fw-bold text-primary mb-0"><xsl:value-of select="$codigo"/></p>
            <h2 class="fw-bold mb-2"><xsl:value-of select="$titulo"/></h2>
            <p class="text-muted mb-4"><xsl:value-of select="$detalle"/></p>
            <a href="/dashboard" class="btn btn-primary px-4">Volver al panel principal</a>
        </div>
    </xsl:template>
</xsl:stylesheet>
