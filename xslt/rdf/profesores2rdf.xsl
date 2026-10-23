<?xml version="1.0" encoding="UTF-8"?>
<!--
  profesores2rdf.xsl  (XSLT 1.0)
  Transforma data/xml/profesores.xml  ->  RDF/XML con el MISMO vocabulario que el resto
  del sistema (ontología academico.ttl, prefijo acad:), de modo que los profesores se
  enlazan con las materias (acad:impartidaPor) y se pueden consultar junto con ellas.

  Por cada <profesor> genera:
    <http://academico.edu.mx/recurso/profesor/P001>  a acad:Profesor
        acad:id, acad:nombre, acad:especialidad, acad:correo, acad:departamento
        acad:imparte  <http://academico.edu.mx/recurso/materia/CCOS005> ...

  Las materias NO se describen aquí (solo se enlazan por su código): su descripción
  vive en materias.xml / materias2rdf.xsl.
-->
<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    xmlns:acad="http://academico.edu.mx/ontologia#">

  <xsl:output method="xml" encoding="UTF-8" indent="yes"/>

  <xsl:template match="/profesores">
    <rdf:RDF>
      <xsl:apply-templates select="profesor"/>
    </rdf:RDF>
  </xsl:template>

  <xsl:template match="profesor">
    <acad:Profesor rdf:about="http://academico.edu.mx/recurso/profesor/{@id}">
      <acad:id><xsl:value-of select="@id"/></acad:id>
      <acad:nombre><xsl:value-of select="normalize-space(nombre)"/></acad:nombre>
      <acad:especialidad><xsl:value-of select="normalize-space(especialidad)"/></acad:especialidad>
      <acad:correo><xsl:value-of select="normalize-space(correo)"/></acad:correo>
      <acad:departamento><xsl:value-of select="normalize-space(departamento)"/></acad:departamento>
      <xsl:for-each select="materias_impartidas/materia">
        <acad:imparte rdf:resource="http://academico.edu.mx/recurso/materia/{@codigo}"/>
      </xsl:for-each>
    </acad:Profesor>
  </xsl:template>

</xsl:stylesheet>
