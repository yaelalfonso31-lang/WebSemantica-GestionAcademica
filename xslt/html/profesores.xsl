<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

    <xsl:output method="html" encoding="UTF-8" indent="yes"/>

    <xsl:template match="/">
        <html lang="es">
            <head>
                <meta charset="UTF-8"/>
                <title>Dashboard Administrador - Profesores</title>
                <script src="https://cdn.tailwindcss.com"></script>
            </head>
            <body class="bg-gray-100 text-gray-800 font-sans p-8">

                <div class="max-w-6xl mx-auto">
                    <header class="mb-8">
                        <h1 class="text-3xl font-bold text-blue-900">Módulo de Profesores</h1>
                        <p class="text-gray-600 mt-2">Sistema Web Semántico - Dashboard Administrativo</p>
                    </header>

                    <!-- Contenedor de la tabla -->
                    <div class="bg-white shadow-lg rounded-lg overflow-hidden border border-gray-200">
                        <table class="min-w-full text-left text-sm whitespace-nowrap">
                            <thead class="bg-blue-50 border-b-2 border-blue-200 text-blue-900 uppercase tracking-wider">
                                <tr>
                                    <th scope="col" class="px-6 py-4 font-semibold">ID</th>
                                    <th scope="col" class="px-6 py-4 font-semibold">Profesor</th>
                                    <th scope="col" class="px-6 py-4 font-semibold">Departamento</th>
                                    <th scope="col" class="px-6 py-4 font-semibold">Materias Impartidas</th>
                                </tr>
                            </thead>
                            <tbody class="divide-y divide-gray-200">

                                <xsl:for-each select="profesores/profesor">
                                    <tr class="hover:bg-gray-50 transition duration-150">

                                        <!-- Obtener el atributo 'id' (nota el uso de la arroba @) -->
                                        <td class="px-6 py-4 text-gray-500 font-mono">
                                            <xsl:value-of select="@id"/>
                                        </td>

                                        <td class="px-6 py-4">
                                            <div class="font-bold text-gray-900 text-base">
                                                <xsl:value-of select="nombre"/>
                                            </div>
                                            <div class="text-xs text-gray-500 mt-1">
                                                <xsl:value-of select="especialidad"/>
                                            </div>
                                            <div class="text-xs text-blue-600 mt-1">
                                                <xsl:value-of select="correo"/>
                                            </div>
                                        </td>

                                        <!-- Departamento con estilo de "badge" (etiqueta) -->
                                        <td class="px-6 py-4">
                                            <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                                                <xsl:value-of select="departamento"/>
                                            </span>
                                        </td>

                                        <!-- Lógica condicional para las materias -->
                                        <td class="px-6 py-4">
                                            <xsl:choose>
                                                <!-- Si tiene materias, crear una lista -->
                                                <xsl:when test="count(materias_impartidas/materia) > 0">
                                                    <ul class="space-y-2">
                                                        <!-- Iteración anidada para las materias -->
                                                        <xsl:for-each select="materias_impartidas/materia">
                                                            <li class="flex items-center text-xs">
                                                                <span class="font-mono bg-gray-200 text-gray-700 px-2 py-1 rounded mr-2 border border-gray-300">
                                                                    <xsl:value-of select="@codigo"/>
                                                                </span>
                                                                <span class="text-gray-800">
                                                                    <xsl:value-of select="."/>
                                                                </span>
                                                            </li>
                                                        </xsl:for-each>
                                                    </ul>
                                                </xsl:when>
                                                <!-- Si no tiene materias, mostrar un mensaje alternativo -->
                                                <xsl:otherwise>
                                                    <span class="text-xs text-gray-400 italic">Sin materias asignadas</span>
                                                </xsl:otherwise>
                                            </xsl:choose>
                                        </td>

                                    </tr>
                                </xsl:for-each>

                            </tbody>
                        </table>
                    </div>
                </div>

            </body>
        </html>
    </xsl:template>
</xsl:stylesheet>