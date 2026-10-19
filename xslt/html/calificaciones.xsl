<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

    <xsl:import href="layout.xsl"/>

    <xsl:template name="content">
        <div class="container mt-4">

            <div class="mb-4 d-flex justify-content-between align-items-center">
                <div>
                    <h2 class="text-success fw-bold mb-1">Captura de Calificaciones</h2>
                    <p class="text-muted">
                        Materia: <span class="badge bg-dark fs-6">
                        <xsl:value-of select="evaluacion/@materia"/>
                    </span> | 
                        Grupo: <span class="text-primary fw-bold">
                    <xsl:value-of select="evaluacion/@grupo"/>
                </span>
            </p>
        </div>
        <a href="/mis_grupos" class="btn btn-outline-secondary shadow-sm">⬅ Volver a Mis Grupos</a>
    </div>

    <div class="card shadow-sm border-0 border-top border-success border-3">
        <div class="card-body p-0">
            <form id="formCalificaciones" onsubmit="guardarCalificaciones(event)">
                <div class="table-responsive">
                    <table class="table table-hover table-striped mb-0 align-middle">
                        <thead class="table-dark">
                            <tr>
                                <th class="px-4">Folio Inscripción</th>
                                <th>Matrícula / Alumno ID</th>
                                <th>Periodo</th>
                                <th style="width: 150px;">Calificación</th>
                                <th style="width: 180px;" class="pe-4">Estatus Final</th>
                            </tr>
                        </thead>
                        <tbody>
                            <xsl:for-each select="evaluacion/inscripcion">
                                <tr>
                                    <td class="px-4 font-monospace text-muted">
                                        <xsl:value-of select="@id"/>
                                    </td>
                                    <td class="fw-bold text-dark">
                                        <xsl:value-of select="alumno_id"/>
                                    </td>
                                    <td>
                                        <xsl:value-of select="periodo"/>
                                    </td>

                                    <!-- Input de Calificación -->
                                    <td>
                                        <input type="number" step="0.1" min="0" max="100" class="form-control calif-input" data-id="{@id}">
                                            <xsl:attribute name="value">
                                                <xsl:value-of select="calificacion_final"/>
                                            </xsl:attribute>
                                        </input>
                                    </td>

                                    <!-- Select de Estatus -->
                                    <td class="pe-4">
                                        <select class="form-select estatus-select" data-id="{@id}">
                                            <option value="Cursando">
                                                <xsl:if test="estatus='Cursando'">
                                                    <xsl:attribute name="selected">selected</xsl:attribute>
                                                </xsl:if>
                                                        Cursando
                                            </option>
                                            <option value="Aprobado">
                                                <xsl:if test="estatus='Aprobado'">
                                                    <xsl:attribute name="selected">selected</xsl:attribute>
                                                </xsl:if>
                                                        Aprobado
                                            </option>
                                            <option value="Reprobado">
                                                <xsl:if test="estatus='Reprobado'">
                                                    <xsl:attribute name="selected">selected</xsl:attribute>
                                                </xsl:if>
                                                        Reprobado
                                            </option>
                                        </select>
                                    </td>
                                </tr>
                            </xsl:for-each>

                            <xsl:if test="count(evaluacion/inscripcion) = 0">
                                <tr>
                                    <td colspan="5" class="text-center py-5 text-muted">
                                                Aún no hay alumnos inscritos en esta materia.
                                    </td>
                                </tr>
                            </xsl:if>
                        </tbody>
                    </table>
                </div>

                <!-- Botón de guardado solo si hay alumnos -->
                <xsl:if test="count(evaluacion/inscripcion) &gt; 0">
                    <div class="p-3 bg-light text-end border-top">
                        <button type="submit" class="btn btn-success fw-bold px-4 shadow-sm">
                                    💾 Guardar Calificaciones
                        </button>
                    </div>
                </xsl:if>
            </form>
        </div>
    </div>
</div>

<!-- Script local para enviar los datos como JSON -->
<script>
            function guardarCalificaciones(event) {
                event.preventDefault();
                const inputsCalif = document.querySelectorAll('.calif-input');
                const selectsEstatus = document.querySelectorAll('.estatus-select');
                
                let datos = {};
                
                // Recopilar datos de todas las filas
                inputsCalif.forEach((input, index) => {
                    let id = input.getAttribute('data-id');
                    let estatus = selectsEstatus[index].value;
                    datos[id] = {
                        calificacion: input.value,
                        estatus: estatus
                    };
                });

                // Enviar al Backend
                fetch('/api/calificar', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(datos)
                })
                .then(response => response.json())
                .then(data => {
                    if(data.error) {
                        alert('❌ Error: ' + data.error);
                    } else {
                        alert('✅ ' + data.mensaje);
                        window.location.reload();
                    }
                })
                .catch(err => {
                    alert('Error de conexión.');
                    console.error(err);
                });
            }
</script>
</xsl:template>
</xsl:stylesheet>