<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

    <xsl:import href="layout.xsl"/>

    <xsl:template name="content">
        <div class="alumnos-page">

            <!-- ============================
                 ENCABEZADO
                 ============================ -->
            <div class="page-header">
                <div class="page-header__text">
                    <div class="page-header__icon">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
                        </svg>
                    </div>
                    <div>
                        <h1 class="page-header__title">Buscador Semántico SPARQL</h1>
                        <p class="page-header__subtitle">
                            Motor de inferencia de conocimiento académico sobre el Grafo RDF
                        </p>
                    </div>
                </div>
                <span class="page-header__badge">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M13 10V3L4 14h7v7l9-11h-7z"/>
                    </svg>
                    Consultas predefinidas
                </span>
            </div>

            <!-- ============================
                 LAYOUT DE DOS COLUMNAS
                 ============================ -->
            <div class="consultas-layout">

                <!-- =====================
                     PANEL DE CONTROL
                     ===================== -->
                <aside class="consultas-sidebar">
                    <div class="panel-card">
                        <div class="panel-card__header">
                            <div class="panel-card__header-icon">
                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/>
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                                </svg>
                            </div>
                            <h2 class="panel-card__title">Opciones de Búsqueda</h2>
                        </div>

                        <div class="panel-card__body">
                            <div class="form-field">
                                <label for="selectConsulta" class="form-label">
                                    Selecciona una consulta
                                </label>
                                <select id="selectConsulta" class="form-input">
                                    <option value="" selected="selected" disabled="disabled">— Elige una consulta —</option>
                                    <option value="alumnos_en_riesgo.rq">Alumnos en Riesgo Académico</option>
                                    <option value="materias_disponibles.rq">Materias Disponibles</option>
                                    <option value="prerrequisitos_de_materia.rq">Prerrequisitos de Materias</option>
                                    <option value="profesores_por_carrera.rq">Profesores por Carrera</option>
                                </select>
                            </div>

                            <button type="button" onclick="lanzarConsultaSPARQL()" class="btn-app btn-app--primary btn-app--block">
                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z"/>
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                                </svg>
                                Ejecutar Consulta
                            </button>
                        </div>
                    </div>

                    <!-- Tarjeta de métricas (oculta hasta ejecutar) -->
                    <div id="panelMetricas" class="metric-panel hidden">
                        <div class="metric-panel__icon">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
                            </svg>
                        </div>
                        <div class="metric-panel__body">
                            <span class="metric-panel__label">Triples inferidos / Resultados</span>
                            <span id="totalResultados" class="metric-panel__value">0</span>
                        </div>
                    </div>
                </aside>

                <!-- =====================
                     PANEL DE RESULTADOS
                     ===================== -->
                <section class="consultas-results">
                    <div class="table-card">
                        <div class="table-card__header">
                            <h2 class="table-card__title">Resultados de la Inferencia</h2>
                            <span id="spinnerCarga" class="loading-spinner hidden" role="status" aria-label="Cargando"></span>
                        </div>

                        <div class="table-scroll">
                            <table class="data-table" id="tablaSPARQL">
                                <thead id="headSPARQL">
                                    <tr>
                                        <th>Esperando ejecución...</th>
                                    </tr>
                                </thead>
                                <tbody id="bodySPARQL">
                                    <tr>
                                        <td colspan="1" class="empty-row">
                                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
                                                <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
                                            </svg>
                                            <p>Selecciona una consulta en el panel izquierdo para comenzar.</p>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </section>

            </div>
        </div>
    </xsl:template>
</xsl:stylesheet>