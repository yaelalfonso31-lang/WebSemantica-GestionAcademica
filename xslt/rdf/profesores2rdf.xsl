<?xml version="1.0" encoding="UTF-8"?>
<!--
  profesores2rdf.xsl  (XSLT 1.0)
  Transforma data/xml/profesores.xml  ->  RDF/XML

  Por cada <profesor> genera:
    ac:Prof_P1001  a ac:Profesor
                   foaf:name, foaf:mbox, ac:idProfesor, ac:especialidad
                   ac:perteneceADepartamento  ac:Dep_Sistemas
                   ac:imparte                 ac:Mat_CS201 ...
  Por cada departamento distinto genera un ac:Departamento con su etiqueta.

  Las materias NO se describen aquí (solo se enlazan por su código):
  su descripción vive en materias.xml / materias2rdf.xsl.

  Parámetro:  base  = namespace de la ontología (por defecto http://ejemplo.edu/academico#)
-->
<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"
    xmlns:foaf="http://xmlns.com/foaf/0.1/"
    xmlns:ac="http://ejemplo.edu/academico#">

  <xsl:output method="xml" encoding="UTF-8" indent="yes"/>

  <xsl:param name="base" select="'http://ejemplo.edu/academico#'"/>

  <!-- Clave para obtener una sola vez cada departamento -->
  <xsl:key name="dep" match="profesor" use="normalize-space(departamento)"/>

  <xsl:template match="/profesores">
    <rdf:RDF>
      <xsl:apply-templates select="profesor"/>

      <!-- Departamentos (uno por cada nombre distinto) -->
      <xsl:for-each select="profesor[generate-id(.) = generate-id(key('dep', normalize-space(departamento))[1])]">
        <ac:Departamento rdf:about="{$base}Dep_{translate(normalize-space(departamento), ' áéíóúñüÁÉÍÓÚÑÜ', '_aeiounuAEIOUNU')}">
          <rdfs:label><xsl:value-of select="normalize-space(departamento)"/></rdfs:label>
        </ac:Departamento>
      </xsl:for-each>
    </rdf:RDF>
  </xsl:template>

  <xsl:template match="profesor">
    <ac:Profesor rdf:about="{$base}Prof_{@id}">
      <ac:idProfesor><xsl:value-of select="@id"/></ac:idProfesor>
      <foaf:name><xsl:value-of select="normalize-space(nombre)"/></foaf:name>
      <foaf:mbox rdf:resource="mailto:{normalize-space(correo)}"/>
      <ac:especialidad><xsl:value-of select="normalize-space(especialidad)"/></ac:especialidad>
      <ac:perteneceADepartamento
          rdf:resource="{$base}Dep_{translate(normalize-space(departamento), ' áéíóúñüÁÉÍÓÚÑÜ', '_aeiounuAEIOUNU')}"/>
      <xsl:for-each select="materias_impartidas/materia">
        <ac:imparte rdf:resource="{$base}Mat_{@codigo}"/>
      </xsl:for-each>
    </ac:Profesor>
  </xsl:template>

</xsl:stylesheet>
