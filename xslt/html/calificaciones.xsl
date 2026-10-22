<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

    <xsl:import href="layout.xsl"/>

    <xsl:template name="content">
        <div class="alumnos-page">

            <div class="page-header">
                <div class="page-header__text">
                    <div class="page-header__icon">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01"/>
                        </svg>
                    </div>
                    <div>
                        <h1 class="page-header__title">Captura de Calificaciones</h1>
                        <p class="page-header__subtitle">
                            <span class="subject-name">
                                <xsl:value-of select="evaluacion/@materia_nombre"/>
                            </span>
                            <span class="subject-sep">·</span>
                            <span class="subject-chip">
                                <xsl:value-of select="evaluacion/@materia"/>
                            </span>
                            <span class="subject-sep">·</span>
                            Grupo <strong>
                            <xsl:value-of select="evaluacion/@grupo"/>
                        </strong>
                    </p>
                </div>
            </div>
            <a href="/mis_grupos" class="btn-app btn-app--ghost">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M10 19l-7-7m0 0l7-7m-7 7h18"/>
                </svg>
                    Volver a mis grupos
            </a>
        </div>

        <div class="info-banner">
            <div class="info-banner__icon">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                </svg>
            </div>
            <div class="info-banner__text">
                    Escala <strong>0 – 100</strong>. Aprueba con <strong>70 o más</strong>. 
                    Deja el campo vacío para dejar al alumno en estatus <em>“Cursando”</em>. 
                    El estatus se calcula automáticamente al guardar.
            </div>
        </div>

        <div class="table-card">

            <div class="table-card__header">
                <h2 class="table-card__title">Lista de Alumnos</h2>
                <span class="table-card__badge">
                    <xsl:value-of select="count(evaluacion/inscripcion)"/>
                    <xsl:text> inscritos</xsl:text>
                </span>
            </div>

            <form id="formCalificaciones" data-grupo="{evaluacion/@grupo}" onsubmit="guardarCalificaciones(event)">

                <div class="table-scroll">
                    <table class="data-table calif-table">
                        <thead>
                            <tr>
                                <th class="calif-col-matricula">Matrícula</th>
                                <th>Alumno</th>
                                <th class="calif-col-periodo">Periodo</th>
                                <th class="calif-col-input text-center">Calificación</th>
                                <th class="calif-col-estatus text-center">Estatus</th>
                            </tr>
                        </thead>
                        <tbody>
                            <xsl:for-each select="evaluacion/inscripcion">
                                <xsl:sort select="alumno_nombre"/>
                                <tr>
                                    <td class="calif-col-matricula">
                                        <span class="matricula">
                                            <xsl:value-of select="matricula"/>
                                        </span>
                                    </td>
                                    <td>
                                        <div class="cell-primary">
                                            <xsl:value-of select="alumno_nombre"/>
                                        </div>
                                    </td>
                                    <td class="calif-col-periodo">
                                        <span class="periodo-chip">
                                            <xsl:value-of select="periodo"/>
                                        </span>
                                    </td>
                                    <td class="calif-col-input text-center">
                                        <input type="number" step="0.1" min="0" max="100" class="calif-input" data-id="{@id}" aria-label="Calificación de {alumno_nombre}">
                                            <xsl:attribute name="value">
                                                <xsl:value-of select="calificacion_final"/>
                                            </xsl:attribute>
                                        </input>
                                    </td>
                                    <td class="calif-col-estatus text-center">
                                        <span class="estatus-badge">
                                            <xsl:value-of select="estatus"/>
                                        </span>
                                    </td>
                                </tr>
                            </xsl:for-each>

                            <xsl:if test="count(evaluacion/inscripcion) = 0">
                                <tr>
                                    <td colspan="5" class="empty-row">
                                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
                                            <path stroke-linecap="round" stroke-linejoin="round" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z"/>
                                        </svg>
                                        <p>Aún no hay alumnos inscritos en este grupo.</p>
                                    </td>
                                </tr>
                            </xsl:if>
                        </tbody>
                    </table>
                </div>

                <xsl:if test="count(evaluacion/inscripcion) &gt; 0">
                    <div class="table-card__actions">
                        <div class="table-card__actions-meta">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                            </svg>
                                Los cambios se aplican al guardar
                        </div>
                        <button type="submit" class="btn-app btn-app--primary">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M8 7H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-3m-1 4l-3 3m0 0l-3-3m3 3V4"/>
                            </svg>
                                Guardar Calificaciones
                        </button>
                    </div>
                </xsl:if>
            </form>
        </div>

    </div>
    <script type="text/javascript">
            //                                                <![CDATA[
            var CALIF_MINIMA = 70;

            /**
             * Actualiza el badge de estatus según el valor del input.
             */
            function pintarEstatus(input) {
                var fila  = input.closest('tr');
                var badge = fila.querySelector('.estatus-badge');
                var valor = input.value.trim();

                var texto = 'Cursando';
                var clase = 'estatus-badge estatus-badge--cursando';

                // Normaliza el input visualmente
                input.classList.remove('is-aprobado', 'is-reprobado');

                if (valor !== '' && !isNaN(valor)) {
                    var num = parseFloat(valor);
                    if (num >= CALIF_MINIMA) {
                        texto = 'Aprobado';
                        clase = 'estatus-badge estatus-badge--aprobado';
                        input.classList.add('is-aprobado');
                    } else {
                        texto = 'Reprobado';
                        clase = 'estatus-badge estatus-badge--reprobado';
                        input.classList.add('is-reprobado');
                    }
                }

                badge.textContent = texto;
                badge.className = clase;
            }

            // Inicializar cada input
            document.querySelectorAll('.calif-input').forEach(function (input) {
                pintarEstatus(input);
                input.addEventListener('input', function () { pintarEstatus(input); });
            });

            /**
             * Envía las calificaciones al backend.
             */
            function guardarCalificaciones(event) {
                event.preventDefault();
                var form = event.target;
                var calificaciones = {};

                document.querySelectorAll('.calif-input').forEach(function (input) {
                    calificaciones[input.getAttribute('data-id')] = input.value;
                });

                fetch('/api/calificar', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        grupo: form.getAttribute('data-grupo'),
                        calificaciones: calificaciones
                    })
                })
                .then(function (r) { return r.json(); })
                .then(function (data) {
                    if (data.error) {
                        alert('Error: ' + data.error);
                    } else {
                        alert('Listo: ' + data.mensaje);
                        window.location.reload();
                    }
                })
                .catch(function () {
                    alert('Error de conexión con el servidor.');
                });
            }
            //]]>
    </script>
</xsl:template>
</xsl:stylesheet>