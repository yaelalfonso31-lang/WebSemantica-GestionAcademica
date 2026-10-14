<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    xmlns:acad="http://academico.edu.mx/ontologia#">

    <xsl:output method="xml" encoding="UTF-8" indent="yes"/>

    <xsl:template match="/alumnos">
        <rdf:RDF>
            <xsl:for-each select="alumno">
                <acad:Alumno rdf:about="http://academico.edu.mx/recurso/alumno/{@id}">
                    <acad:id>
                        <xsl:value-of select="@id"/>
                    </acad:id>
                    <acad:matricula>
                        <xsl:value-of select="@matricula"/>
                    </acad:matricula>
                    <acad:nombre>
                        <xsl:value-of select="nombre"/>
                    </acad:nombre>
                    <acad:apellidos>
                        <xsl:value-of select="apellidos"/>
                    </acad:apellidos>
                    <acad:correo>
                        <xsl:value-of select="correo"/>
                    </acad:correo>
                    <acad:semestre rdf:datatype="http://www.w3.org/2001/XMLSchema#integer">
                        <xsl:value-of select="semestre"/>
                    </acad:semestre>
                    <acad:promedio rdf:datatype="http://www.w3.org/2001/XMLSchema#decimal">
                        <xsl:value-of select="promedio"/>
                    </acad:promedio>
                    <acad:estatus>
                        <xsl:value-of select="estatus"/>
                    </acad:estatus>
                    <acad:perteneceACarrera rdf:resource="http://academico.edu.mx/recurso/carrera/{carrera_id}"/>
                </acad:Alumno>
            </xsl:for-each>
        </rdf:RDF>
    </xsl:template>
</xsl:stylesheet>