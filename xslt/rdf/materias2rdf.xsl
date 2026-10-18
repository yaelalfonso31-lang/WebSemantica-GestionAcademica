<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    xmlns:acad="http://academico.edu.mx/ontologia#">

    <xsl:output method="xml" encoding="UTF-8" indent="yes"/>

    <xsl:template match="/materias">
        <rdf:RDF>
            <xsl:for-each select="materia">
                <acad:Materia rdf:about="http://academico.edu.mx/recurso/materia/{@id}">
                    <acad:id>
                        <xsl:value-of select="@id"/>
                    </acad:id>
                    <acad:clave>
                        <xsl:value-of select="@clave"/>
                    </acad:clave>
                    <acad:nombre>
                        <xsl:value-of select="normalize-space(nombre)"/>
                    </acad:nombre>
                    <acad:descripcion>
                        <xsl:value-of select="normalize-space(descripcion)"/>
                    </acad:descripcion>
                    <acad:creditos rdf:datatype="http://www.w3.org/2001/XMLSchema#integer">
                        <xsl:value-of select="normalize-space(creditos)"/>
                    </acad:creditos>
                    <acad:semestre rdf:datatype="http://www.w3.org/2001/XMLSchema#integer">
                        <xsl:value-of select="normalize-space(semestre)"/>
                    </acad:semestre>
                    <acad:perteneceACarrera rdf:resource="http://academico.edu.mx/recurso/carrera/{carrera/@codigo}"/>
                    <acad:impartidaPor rdf:resource="http://academico.edu.mx/recurso/profesor/{profesor/@id}"/>

                    <!-- Relación hacia las materias prerrequisito -->
                    <xsl:for-each select="prerrequisitos/prerrequisito">
                        <acad:tienePrerrequisito rdf:resource="http://academico.edu.mx/recurso/materia/{@ref}"/>
                    </xsl:for-each>
                </acad:Materia>
            </xsl:for-each>
        </rdf:RDF>
    </xsl:template>
</xsl:stylesheet>