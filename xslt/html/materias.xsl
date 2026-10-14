<?xml version="1.0" encoding="UTF-8"?>

<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

    <xsl:output method="html" encoding="UTF-8" indent="yes"/>


    <xsl:template match="/">

        <html>

            <head>

                <meta charset="UTF-8"/>

                <title>
                    Catálogo de Materias
                </title>

                <style>

                    body {
                        font-family: Arial, sans-serif;
                        margin: 0;
                        padding: 30px;
                        background: #f4f6f8;
                    }

                    h1 {
                        text-align: center;
                        color: #243447;
                    }

                    .subtitulo {
                        text-align: center;
                        color: #555;
                        margin-bottom: 30px;
                    }

                    table {
                        width: 100%;
                        border-collapse: collapse;
                        background: white;
                    }

                    th {
                        background: #243447;
                        color: white;
                        padding: 12px;
                    }

                    td {
                        padding: 12px;
                        border: 1px solid #ddd;
                        vertical-align: top;
                    }

                    tr:nth-child(even) {
                        background: #f8f9fa;
                    }

                    .codigo {
                        font-weight: bold;
                        white-space: nowrap;
                    }

                    .numero {
                        text-align: center;
                    }

                    .prerrequisitos {
                        margin: 0;
                        padding-left: 20px;
                    }

                    .total {
                        margin-top: 20px;
                        font-weight: bold;
                    }

                </style>

            </head>


            <body>

                <h1>
                    Catálogo de Materias
                </h1>

                <p class="subtitulo">
                    Ingeniería en Ciencias de la Computación
                </p>


                <table>

                    <thead>

                        <tr>

                            <th>Clave</th>
                            <th>Materia</th>
                            <th>Descripción</th>
                            <th>Créditos</th>
                            <th>Semestre</th>
                            <th>Carrera</th>
                            <th>Profesor</th>
                            <th>Prerrequisitos</th>

                        </tr>

                    </thead>


                    <tbody>

                        <xsl:for-each select="materias/materia">

                            <xsl:sort select="semestre" data-type="number"/>


                            <tr>

                                <td class="codigo">
                                    <xsl:value-of select="@clave"/>
                                </td>


                                <td>
                                    <xsl:value-of select="nombre"/>
                                </td>


                                <td>
                                    <xsl:value-of select="descripcion"/>
                                </td>


                                <td class="numero">
                                    <xsl:value-of select="creditos"/>
                                </td>


                                <td class="numero">
                                    <xsl:value-of select="semestre"/>
                                </td>


                                <td>
                                    <xsl:value-of select="carrera"/>
                                </td>


                                <td>
                                    <xsl:value-of select="profesor"/>
                                </td>


                                <td>

                                    <xsl:choose>

                                        <xsl:when test="prerrequisitos/prerrequisito">

                                            <ul class="prerrequisitos">

                                                <xsl:for-each select="prerrequisitos/prerrequisito">

                                                    <li>

                                                        <xsl:value-of select="@nombre"/>

                                                    </li>

                                                </xsl:for-each>

                                            </ul>

                                        </xsl:when>


                                        <xsl:otherwise>

                                            Ninguno

                                        </xsl:otherwise>

                                    </xsl:choose>

                                </td>

                            </tr>

                        </xsl:for-each>

                    </tbody>

                </table>


                <p class="total">

                    Total de materias:

                    <xsl:value-of select="count(materias/materia)"/>

                </p>

            </body>

        </html>

    </xsl:template>

</xsl:stylesheet>