<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:import href="layout.xsl"/>

    <xsl:template name="content">
        <div class="alumnos-page">

            <div class="page-header">
                <div class="page-header__text">
                    <div class="page-header__icon">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
                        </svg>
                    </div>
                    <div>
                        <h1 class="page-header__title">Grupos e Inscripciones</h1>
                        <p class="page-header__subtitle">Periodo: <xsl:value-of select="grupos_admin/@periodo"/></p>
                    </div>
                </div>
                <button type="button" class="btn btn-warning fw-bold" data-bs-toggle="modal" data-bs-target="#modalGrupo">+ Nuevo grupo</button>
            </div>

            <div class="grupos-admin">
                <table class="table table-hover align-middle mb-0">
                    <thead>
                        <tr>
                            <th>Grupo</th>
                            <th>Materia</th>
                            <th>Profesor</th>
                            <th>Horario</th>
                            <th>Aula</th>
                            <th class="text-center">Inscritos</th>
                            <th class="text-end">Acciones</th>
                        </tr>
                    </thead>
                    <tbody>
                        <xsl:for-each select="grupos_admin/grupo">
                            <tr>
                                <td><span class="horario-chip"><xsl:value-of select="@id"/></span></td>
                                <td>
                                    <strong><xsl:value-of select="materia_nombre"/></strong>
                                    <div class="small text-muted"><xsl:value-of select="materia_id"/></div>
                                </td>
                                <td><xsl:value-of select="profesor_nombre"/></td>
                                <td>
                                    <xsl:value-of select="dia"/>
                                    <div class="small text-muted"><xsl:value-of select="hora_inicio"/> – <xsl:value-of select="hora_fin"/></div>
                                </td>
                                <td><xsl:value-of select="aula"/></td>
                                <td class="text-center"><span class="badge bg-primary"><xsl:value-of select="count(inscritos/inscripcion)"/></span></td>
                                <td class="text-end text-nowrap">
                                    <button type="button" class="btn btn-sm btn-outline-secondary" data-bs-toggle="collapse" data-bs-target="#det-{@id}">Alumnos</button>
                                    <button type="button" class="btn btn-sm btn-outline-primary" data-bs-toggle="modal" data-bs-target="#modalInscribir" onclick="prepararInscripcion('{@id}')">Inscribir</button>
                                    <button type="button" class="btn btn-sm btn-outline-danger" onclick="eliminarGrupo('{@id}')">Eliminar</button>
                                </td>
                            </tr>
                            <tr class="collapse grupos-admin__detalle" id="det-{@id}">
                                <td colspan="7">
                                    <xsl:choose>
                                        <xsl:when test="count(inscritos/inscripcion) = 0">
                                            <span class="text-muted">Sin alumnos inscritos.</span>
                                        </xsl:when>
                                        <xsl:otherwise>
                                            <ul class="grupos-admin__lista">
                                                <xsl:for-each select="inscritos/inscripcion">
                                                    <li>
                                                        <span><strong><xsl:value-of select="@alumno"/></strong>
                                                            <span class="text-muted"> · <xsl:value-of select="@matricula"/></span></span>
                                                        <span>
                                                            <span class="badge">
                                                                <xsl:attribute name="class">badge <xsl:choose>
                                                                    <xsl:when test="@estatus = 'Aprobado'">bg-success</xsl:when>
                                                                    <xsl:when test="@estatus = 'Reprobado'">bg-danger</xsl:when>
                                                                    <xsl:otherwise>bg-warning text-dark</xsl:otherwise>
                                                                </xsl:choose></xsl:attribute>
                                                                <xsl:value-of select="@estatus"/>
                                                                <xsl:if test="@calificacion != ''"> · <xsl:value-of select="@calificacion"/></xsl:if>
                                                            </span>
                                                            <xsl:if test="@estatus = 'Cursando'">
                                                                <button type="button" class="btn btn-sm btn-link text-danger" onclick="darDeBaja('{@id}')">Dar de baja</button>
                                                            </xsl:if>
                                                        </span>
                                                    </li>
                                                </xsl:for-each>
                                            </ul>
                                        </xsl:otherwise>
                                    </xsl:choose>
                                </td>
                            </tr>
                        </xsl:for-each>
                    </tbody>
                </table>
            </div>
        </div>

        <!-- Modal: nuevo grupo -->
        <div class="modal fade" id="modalGrupo" tabindex="-1" aria-hidden="true">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header"><h5 class="modal-title">Nuevo grupo</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Cerrar"></button></div>
                    <div class="modal-body">
                        <div id="errorGrupo" class="alert alert-danger d-none"></div>
                        <div class="mb-2"><label class="form-label">Materia</label>
                            <select id="g_materia" class="form-select">
                                <xsl:for-each select="grupos_admin/catalogos/materia">
                                    <option value="{@id}"><xsl:value-of select="@id"/> · <xsl:value-of select="."/></option>
                                </xsl:for-each>
                            </select></div>
                        <div class="mb-2"><label class="form-label">Profesor</label>
                            <select id="g_profesor" class="form-select">
                                <xsl:for-each select="grupos_admin/catalogos/profesor">
                                    <option value="{@id}"><xsl:value-of select="."/> (<xsl:value-of select="@id"/>)</option>
                                </xsl:for-each>
                            </select></div>
                        <div class="row g-2 mb-2">
                            <div class="col-6"><label class="form-label">Periodo</label>
                                <input id="g_periodo" class="form-control" value="{grupos_admin/@periodo}"/></div>
                            <div class="col-6"><label class="form-label">Días</label>
                                <select id="g_dia" class="form-select">
                                    <option>Lunes y Miércoles</option><option>Martes y Jueves</option>
                                    <option>Viernes</option><option>Lunes, Miércoles y Viernes</option><option>Sábado</option>
                                </select></div>
                        </div>
                        <div class="row g-2 mb-2">
                            <div class="col-6"><label class="form-label">Hora de inicio</label>
                                <input id="g_inicio" type="time" class="form-control" value="07:00"/></div>
                            <div class="col-6"><label class="form-label">Hora de fin</label>
                                <input id="g_fin" type="time" class="form-control" value="09:00"/></div>
                        </div>
                        <div class="mb-2"><label class="form-label">Aula</label>
                            <input id="g_aula" class="form-control" placeholder="Edificio 1 - Aula 101"/></div>
                        <p class="small text-muted mb-0">El sistema impide traslapes de horario del profesor y del aula.</p>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
                        <button type="button" class="btn btn-primary" onclick="crearGrupo()">Crear grupo</button>
                    </div>
                </div>
            </div>
        </div>

        <!-- Modal: inscribir alumno -->
        <div class="modal fade" id="modalInscribir" tabindex="-1" aria-hidden="true">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header"><h5 class="modal-title">Inscribir alumno en <span id="i_grupo_txt"></span></h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Cerrar"></button></div>
                    <div class="modal-body">
                        <div id="errorInscribir" class="alert alert-danger d-none"></div>
                        <input type="hidden" id="i_grupo"/>
                        <label class="form-label">Alumno</label>
                        <select id="i_alumno" class="form-select">
                            <xsl:for-each select="grupos_admin/catalogos/alumno">
                                <option value="{@id}"><xsl:value-of select="."/> · <xsl:value-of select="@matricula"/></option>
                            </xsl:for-each>
                        </select>
                        <p class="small text-muted mt-2 mb-0">Se valida que no haya choques de horario, que se cumplan los prerrequisitos y que la materia no esté aprobada o en curso.</p>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
                        <button type="button" class="btn btn-primary" onclick="inscribirAlumno()">Inscribir</button>
                    </div>
                </div>
            </div>
        </div>

        <script>
            function mostrarError(id, msg) { const e = document.getElementById(id); e.textContent = msg; e.classList.remove('d-none'); }

            function enviar(url, metodo, cuerpo, idError) {
                return fetch(url, { method: metodo, headers: { 'Content-Type': 'application/json' },
                                    body: cuerpo ? JSON.stringify(cuerpo) : undefined })
                    .then(function (r) { return r.json().then(function (d) { return { ok: r.ok, d: d }; }); })
                    .then(function (x) {
                        if (!x.ok) { if (idError) { mostrarError(idError, x.d.error); } else { alert(x.d.error); } return false; }
                        window.location.reload(); return true;
                    })
                    .catch(function () { if (idError) { mostrarError(idError, 'Error de conexión con el servidor.'); } else { alert('Error de conexión con el servidor.'); } });
            }

            function crearGrupo() {
                enviar('/api/grupos', 'POST', {
                    materia_id: document.getElementById('g_materia').value, profesor_id: document.getElementById('g_profesor').value,
                    periodo: document.getElementById('g_periodo').value, dia: document.getElementById('g_dia').value,
                    hora_inicio: document.getElementById('g_inicio').value, hora_fin: document.getElementById('g_fin').value,
                    aula: document.getElementById('g_aula').value }, 'errorGrupo');
            }

            function prepararInscripcion(grupo) {
                document.getElementById('i_grupo').value = grupo;
                document.getElementById('i_grupo_txt').textContent = grupo;
                document.getElementById('errorInscribir').classList.add('d-none');
            }

            function inscribirAlumno() {
                enviar('/api/inscripciones', 'POST', { alumno_id: document.getElementById('i_alumno').value,
                                                       grupo_id: document.getElementById('i_grupo').value }, 'errorInscribir');
            }

            function eliminarGrupo(id) { if (confirm('¿Eliminar el grupo ' + id + '?')) { enviar('/api/grupos/' + id, 'DELETE'); } }
            function darDeBaja(id) { if (confirm('¿Dar de baja esta inscripción?')) { enviar('/api/inscripciones/' + id, 'DELETE'); } }
        </script>
    </xsl:template>
</xsl:stylesheet>
