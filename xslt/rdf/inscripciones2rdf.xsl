<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    xmlns:acad="http://academico.edu.mx/ontologia#">

    <xsl:output method="xml" encoding="UTF-8" indent="yes"/>

    <xsl:template match="/inscripciones">
        <rdf:RDF>
            <xsl:for-each select="inscripcion">
                <!-- El sujeto de la tripleta es la Inscripción misma -->
                <acad:Inscripcion rdf:about="http://academico.edu.mx/recurso/inscripcion/{@id}">

                    <acad:id>
                        <xsl:value-of select="@id"/>
                    </acad:id>
                    <acad:periodo>
                        <xsl:value-of select="periodo"/>
                    </acad:periodo>
                    <acad:estatus>
                        <xsl:value-of select="estatus"/>
                    </acad:estatus>

                    <xsl:if test="calificacion_final != ''">
                        <acad:calificacionFinal rdf:datatype="http://www.w3.org/2001/XMLSchema#decimal">
                            <xsl:value-of select="calificacion_final"/>
                        </acad:calificacionFinal>
                    </xsl:if>

                    <!-- Relaciones (Object Properties) -->
                    <acad:realizadaPor rdf:resource="http://academico.edu.mx/recurso/alumno/{alumno_id}"/>
                    <acad:inscribeA rdf:resource="http://academico.edu.mx/recurso/materia/{materia_id}"/>

                </acad:Inscripcion>

                <!-- Inferencia directa: Si hay inscripción, el alumno cursa la materia -->
                <acad:Alumno rdf:about="http://academico.edu.mx/recurso/alumno/{alumno_id}">
                    <acad:cursaMateria rdf:resource="http://academico.edu.mx/recurso/materia/{materia_id}"/>
                </acad:Alumno>

            </xsl:for-each>
        </rdf:RDF>
    </xsl:template>
</xsl:stylesheet>