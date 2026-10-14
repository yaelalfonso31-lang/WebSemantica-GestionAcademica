<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

    <xsl:output method="html" encoding="UTF-8" indent="yes"/>

    <xsl:template match="/">
        <html lang="es">
            <head>
                <meta charset="UTF-8"/>
                <title>Dashboard Administrador - Alumnos</title>
                <script src="https://cdn.tailwindcss.com"></script>
            </head>
            <body class="bg-gray-100 text-gray-800 font-sans p-8">

                <div class="max-w-6xl mx-auto">
                    <header class="mb-8">
                        <h1 class="text-3xl font-bold text-blue-900">Módulo de Alumnos</h1>
                        <p class="text-gray-600 mt-2">EduSemantic - Sistema Web Semántico de Gestión Académica</p>
                    </header>

                    <!-- Resumen rápido con XPath -->
                    <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
                        <div class="bg-white p-4 rounded-lg shadow border border-gray-200">
                            <span class="text-xs font-semibold uppercase text-gray-500">Total de Alumnos</span>
                            <p class="text-2xl font-bold text-blue-900 mt-1">
                                <xsl:value-of select="count(alumnos/alumno)"/>
                            </p>
                        </div>
                        <div class="bg-white p-4 rounded-lg shadow border border-gray-200">
                            <span class="text-xs font-semibold uppercase text-gray-500">Promedio General</span>
                            <p class="text-2xl font-bold text-green-700 mt-1">
                                <xsl:value-of select="format-number(sum(alumnos/alumno/promedio) div count(alumnos/alumno), '0.0')"/>
                            </p>
                        </div>
                        <div class="bg-white p-4 rounded-lg shadow border border-gray-200">
                            <span class="text-xs font-semibold uppercase text-gray-500">Alumnos Activos</span>
                            <p class="text-2xl font-bold text-indigo-700 mt-1">
                                <xsl:value-of select="count(alumnos/alumno[estatus='Activo'])"/>
                            </p>
                        </div>
                    </div>

                    <!-- Contenedor de la tabla -->
                    <div class="bg-white shadow-lg rounded-lg overflow-hidden border border-gray-200">
                        <table class="min-w-full text-left text-sm whitespace-nowrap">
                            <thead class="bg-blue-50 border-b-2 border-blue-200 text-blue-900 uppercase tracking-wider">
                                <tr>
                                    <th scope="col" class="px-6 py-4 font-semibold">ID / Matrícula</th>
                                    <th scope="col" class="px-6 py-4 font-semibold">Alumno</th>
                                    <th scope="col" class="px-6 py-4 font-semibold">Carrera</th>
                                    <th scope="col" class="px-6 py-4 font-semibold">Semestre</th>
                                    <th scope="col" class="px-6 py-4 font-semibold">Promedio</th>
                                    <th scope="col" class="px-6 py-4 font-semibold">Estatus</th>
                                </tr>
                            </thead>
                            <tbody class="divide-y divide-gray-200">

                                <xsl:for-each select="alumnos/alumno">
                                    <tr class="hover:bg-gray-50 transition duration-150">

                                        <!-- ID (atributo @id) y Matrícula -->
                                        <td class="px-6 py-4">
                                            <div class="font-mono font-semibold text-gray-800">
                                                <xsl:value-of select="matricula"/>
                                            </div>
                                            <div class="text-xs text-gray-400 font-mono mt-0.5">
                                                ID: <xsl:value-of select="@id"/>
                                            </div>
                                        </td>

                                        <!-- Nombre y Correo -->
                                        <td class="px-6 py-4">
                                            <div class="font-bold text-gray-900 text-base">
                                                <xsl:value-of select="nombre"/>
                                            </div>
                                            <div class="text-xs text-blue-600 mt-1">
                                                <xsl:value-of select="correo"/>
                                            </div>
                                        </td>

                                        <!-- Carrera y su atributo @id -->
                                        <td class="px-6 py-4">
                                            <div class="flex items-center">
                                                <span class="font-mono text-xs bg-gray-200 text-gray-700 px-2 py-0.5 rounded mr-2 border border-gray-300">
                                                    <xsl:value-of select="carrera/@id"/>
                                                </span>
                                                <span class="text-gray-800 font-medium">
                                                    <xsl:value-of select="carrera"/>
                                                </span>
                                            </div>
                                        </td>

                                        <!-- Semestre -->
                                        <td class="px-6 py-4 text-gray-600">
                                            Semestre <xsl:value-of select="semestre"/>
                                        </td>

                                        <!-- Promedio formateado a un decimal -->
                                        <td class="px-6 py-4 font-mono font-bold text-gray-900">
                                            <xsl:value-of select="format-number(promedio, '0.0')"/>
                                        </td>

                                        <!-- Lógica condicional para el Estatus -->
                                        <td class="px-6 py-4">
                                            <xsl:choose>
                                                <xsl:when test="estatus = 'Activo'">
                                                    <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                                                        <xsl:value-of select="estatus"/>
                                                    </span>
                                                </xsl:when>
                                                <xsl:when test="estatus = 'Egresado'">
                                                    <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                                                        <xsl:value-of select="estatus"/>
                                                    </span>
                                                </xsl:when>
                                                <xsl:otherwise>
                                                    <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-200 text-gray-700">
                                                        <xsl:value-of select="estatus"/>
                                                    </span>
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