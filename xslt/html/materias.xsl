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
                            <path stroke-linecap="round" stroke-linejoin="round" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"/>
                        </svg>
                    </div>
                    <div>
                        <h1 class="page-header__title">Módulo de Materias</h1>
                        <p class="page-header__subtitle">
                            EduSemantic · Catálogo de asignaturas y seriación
                        </p>
                    </div>
                </div>
                <button type="button" onclick="abrirModalMateria()" class="btn-app btn-app--primary">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4"/>
                    </svg>
                    Nueva Materia
                </button>
            </div>
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-card__icon">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"/>
                        </svg>
                    </div>
                    <div class="stat-card__body">
                        <span class="stat-card__label">Total de Materias</span>
                        <span class="stat-card__value">
                            <xsl:value-of select="count(materias/materia)"/>
                        </span>
                    </div>
                </div>

                <div class="stat-card">
                    <div class="stat-card__icon">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z"/>
                        </svg>
                    </div>
                    <div class="stat-card__body">
                        <span class="stat-card__label">Total de Créditos</span>
                        <span class="stat-card__value">
                            <xsl:value-of select="sum(materias/materia/creditos)"/>
                        </span>
                    </div>
                </div>

                <div class="stat-card">
                    <div class="stat-card__icon">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1"/>
                        </svg>
                    </div>
                    <div class="stat-card__body">
                        <span class="stat-card__label">Con Seriación</span>
                        <span class="stat-card__value">
                            <xsl:value-of select="count(materias/materia[prerrequisitos/prerrequisito])"/>
                        </span>
                    </div>
                </div>
            </div>


            <div class="table-card">
                <div class="table-card__header">
                    <h2 class="table-card__title">Catálogo de Materias</h2>
                    <span class="table-card__badge">
                        <xsl:value-of select="count(materias/materia)"/>
                            registros
                    </span>
                </div>

                <div class="table-scroll">
                    <table class="data-table">
                        <thead>
                            <tr>
                                <th>Clave / ID</th>
                                <th>Asignatura</th>
                                <th>Semestre / Créditos</th>
                                <th>Carrera</th>
                                <th>Profesor</th>
                                <th>Prerrequisitos</th>
                                <th class="text-right">Acciones</th>
                            </tr>
                        </thead>
                        <tbody>
                            <xsl:for-each select="materias/materia">
                                <xsl:sort select="semestre" data-type="number"/>
                                <tr>
                                    <td>
                                        <span class="chip">
                                            <xsl:value-of select="@clave"/>
                                        </span>
                                        <div class="cell-secondary">
                                            ID: <xsl:value-of select="@id"/>
                                        </div>
                                    </td>

                                    <td>
                                        <div class="cell-primary">
                                            <xsl:value-of select="normalize-space(nombre)"/>
                                        </div>
                                        <div class="cell-secondary">
                                            <xsl:value-of select="normalize-space(descripcion)"/>
                                        </div>
                                    </td>

                                    <td>
                                        <div class="cell-primary">
                                            <xsl:value-of select="normalize-space(semestre)"/>
º semestre
                                        </div>
                                        <div class="cell-secondary">
                                            <xsl:value-of select="normalize-space(creditos)"/>
 créditos
                                        </div>
                                    </td>

                                    <td>
                                        <span class="chip">
                                            <xsl:value-of select="carrera/@codigo"/>
                                        </span>
                                    </td>

                                    <td>
                                        <div class="cell-primary">
                                            <xsl:value-of select="normalize-space(profesor)"/>
                                        </div>
                                        <div class="cell-secondary">
                                            ID: <xsl:value-of select="profesor/@id"/>
                                        </div>
                                    </td>

                                    <td>
                                        <xsl:choose>
                                            <xsl:when test="prerrequisitos/prerrequisito">
                                                <ul class="req-list">
                                                    <xsl:for-each select="prerrequisitos/prerrequisito">
                                                        <li class="req-list__item">
                                                            <span class="req-list__code">
                                                                <xsl:value-of select="@ref"/>
                                                            </span>
                                                            <span class="req-list__name">
                                                                <xsl:value-of select="@nombre"/>
                                                            </span>
                                                        </li>
                                                    </xsl:for-each>
                                                </ul>
                                            </xsl:when>
                                            <xsl:otherwise>
                                                <span class="cell-secondary">Ninguno</span>
                                            </xsl:otherwise>
                                        </xsl:choose>
                                    </td>

                                    <td class="text-right">
                                        <div class="actions">
                                            <button type="button" class="btn-action btn-action--edit" title="Editar materia" onclick="abrirModalEditarMateria('{@id}', '{normalize-space(nombre)}', '{creditos}', '{prerrequisitos/prerrequisito[1]/@ref}')">
                                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                                                    <path stroke-linecap="round" stroke-linejoin="round" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
                                                </svg>
                                                Editar
                                            </button>
                                            <button type="button" class="btn-action btn-action--delete" title="Eliminar materia" onclick="eliminarMateria('{@id}')">
                                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                                                    <path stroke-linecap="round" stroke-linejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                                                </svg>
                                                Eliminar
                                            </button>
                                        </div>
                                    </td>
                                </tr>
                            </xsl:for-each>

                            <xsl:if test="not(materias/materia)">
                                <tr>
                                    <td colspan="7" class="empty-row">
                                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
                                            <path stroke-linecap="round" stroke-linejoin="round" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"/>
                                        </svg>
                                        <p>No hay materias registradas.</p>
                                        <button type="button" onclick="abrirModalMateria()" class="btn-app btn-app--primary">
                                            Registrar la primera
                                        </button>
                                    </td>
                                </tr>
                            </xsl:if>
                        </tbody>
                    </table>
                </div>
            </div>


            <div id="modalNuevaMateria" class="app-modal-overlay hidden">
                <div class="app-modal">
                    <div class="app-modal__header">
                        <div class="app-modal__header-icon">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"/>
                            </svg>
                        </div>
                        <div class="app-modal__header-text">
                            <h3 class="app-modal__title">Registrar Nueva Materia</h3>
                            <p class="app-modal__subtitle">Completa los datos de la asignatura</p>
                        </div>
                        <button type="button" onclick="cerrarModalMateria()" class="app-modal__close" aria-label="Cerrar">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12"/>
                            </svg>
                        </button>
                    </div>

                    <form id="formNuevaMateria" onsubmit="guardarMateria(event)">
                        <div class="app-modal__body">

                            <div class="form-grid form-grid--2">
                                <div class="form-field">
                                    <label for="mat_id" class="form-label">ID de la Materia</label>
                                    <input type="text" id="mat_id" pattern="(CCOS|ICCS)[0-9]{{3}}" placeholder="Ej. CCOS260" required="required" class="form-input"/>
                                </div>
                                <div class="form-field">
                                    <label for="mat_clave" class="form-label">Clave</label>
                                    <input type="text" id="mat_clave" pattern="(CCOS|ICCS) [0-9]{{3}}" placeholder="Ej. CCOS 260" required="required" class="form-input"/>
                                </div>
                            </div>

                            <div class="form-field">
                                <label for="mat_nombre" class="form-label">Nombre de la Asignatura</label>
                                <input type="text" id="mat_nombre" required="required" class="form-input"/>
                            </div>

                            <div class="form-field">
                                <label for="mat_descripcion" class="form-label">Descripción</label>
                                <input type="text" id="mat_descripcion" required="required" class="form-input"/>
                            </div>

                            <div class="form-grid form-grid--2">
                                <div class="form-field">
                                    <label for="mat_creditos" class="form-label">Créditos (1 - 10)</label>
                                    <input type="number" id="mat_creditos" min="1" max="10" value="6" required="required" class="form-input"/>
                                </div>
                                <div class="form-field">
                                    <label for="mat_semestre" class="form-label">Semestre (1 - 10)</label>
                                    <input type="number" id="mat_semestre" min="1" max="10" value="5" required="required" class="form-input"/>
                                </div>
                            </div>

                            <div class="form-grid form-grid--2">
                                <div class="form-field">
                                    <label for="mat_profesor_id" class="form-label">ID Profesor</label>
                                    <input type="text" id="mat_profesor_id" pattern="P[0-9]{{3}}" placeholder="Ej. P001" value="P001" required="required" class="form-input"/>
                                </div>
                                <div class="form-field">
                                    <label for="mat_profesor_nombre" class="form-label">Nombre del Profesor</label>
                                    <input type="text" id="mat_profesor_nombre" required="required" class="form-input"/>
                                </div>
                            </div>

                            <div class="form-field">
                                <label for="mat_prerrequisitos" class="form-label">
                                    Prerrequisitos
                                    <span class="form-label__hint">Ctrl + Clic para seleccionar varios</span>
                                </label>
                                <select id="mat_prerrequisitos" multiple="multiple" size="5" class="form-input form-select-multiple">
                                    <xsl:for-each select="materias/materia">
                                        <option value="{@id}">
                                            <xsl:value-of select="@id"/>
 —                                            <xsl:value-of select="normalize-space(nombre)"/>
                                        </option>
                                    </xsl:for-each>
                                </select>
                            </div>

                        </div>

                        <div class="app-modal__footer">
                            <button type="button" onclick="cerrarModalMateria()" class="btn-app btn-app--ghost">
                                Cancelar
                            </button>
                            <button type="submit" class="btn-app btn-app--primary">
                                Guardar Materia
                            </button>
                        </div>
                    </form>
                </div>
            </div>


            <div id="modalEditarMateria" class="app-modal-overlay hidden">
                <div class="app-modal">
                    <div class="app-modal__header">
                        <div class="app-modal__header-icon app-modal__header-icon--gold">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
                            </svg>
                        </div>
                        <div class="app-modal__header-text">
                            <h3 class="app-modal__title">Editar Materia</h3>
                            <p class="app-modal__subtitle">Actualiza los datos de la asignatura</p>
                        </div>
                        <button type="button" onclick="cerrarModalEditarMateria()" class="app-modal__close" aria-label="Cerrar">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12"/>
                            </svg>
                        </button>
                    </div>

                    <form onsubmit="actualizarMateria(event)">
                        <div class="app-modal__body">
                            <input type="hidden" id="edit_mat_id" />

                            <div class="form-field">
                                <label for="edit_mat_nombre" class="form-label">Nombre de la Materia</label>
                                <input type="text" id="edit_mat_nombre" class="form-input" required="required"/>
                            </div>

                            <div class="form-grid form-grid--2">
                                <div class="form-field">
                                    <label for="edit_mat_creditos" class="form-label">Créditos</label>
                                    <input type="number" id="edit_mat_creditos" class="form-input" min="1" max="20" required="required"/>
                                </div>
                                <div class="form-field">
                                    <label for="edit_mat_prerrequisito" class="form-label">Prerrequisito (ID)</label>
                                    <input type="text" id="edit_mat_prerrequisito" class="form-input" placeholder="Ej. CCOS101"/>
                                    <small class="form-help">Clave de la materia obligatoria previa. Déjalo vacío si no aplica.</small>
                                </div>
                            </div>
                        </div>

                        <div class="app-modal__footer">
                            <button type="button" onclick="cerrarModalEditarMateria()" class="btn-app btn-app--ghost">
                                Cancelar
                            </button>
                            <button type="submit" class="btn-app btn-app--primary">
                                Guardar Cambios
                            </button>
                        </div>
                    </form>
                </div>
            </div>

        </div>

        <!-- Scripts del módulo -->
        <script type="text/javascript">
            //                                                                        <![CDATA[
            function abrirModalMateria() {
                document.getElementById('modalNuevaMateria').classList.remove('hidden');
                document.body.classList.add('modal-open');
            }
            function cerrarModalMateria() {
                document.getElementById('modalNuevaMateria').classList.add('hidden');
                document.body.classList.remove('modal-open');
            }

            function abrirModalEditarMateria(id, nombre, creditos, prerrequisito) {
                document.getElementById('edit_mat_id').value            = id;
                document.getElementById('edit_mat_nombre').value        = nombre;
                document.getElementById('edit_mat_creditos').value      = creditos;
                document.getElementById('edit_mat_prerrequisito').value = prerrequisito || '';
                document.getElementById('modalEditarMateria').classList.remove('hidden');
                document.body.classList.add('modal-open');
            }
            function cerrarModalEditarMateria() {
                document.getElementById('modalEditarMateria').classList.add('hidden');
                document.body.classList.remove('modal-open');
            }

            async function guardarMateria(e) {
                e.preventDefault();
                const selectPrerreq = document.getElementById('mat_prerrequisitos');
                const prerrequisitos = Array.from(selectPrerreq.selectedOptions).map(opt => opt.value);

                const payload = {
                    id: document.getElementById('mat_id').value.trim(),
                    clave: document.getElementById('mat_clave').value.trim(),
                    nombre: document.getElementById('mat_nombre').value.trim(),
                    descripcion: document.getElementById('mat_descripcion').value.trim(),
                    creditos: document.getElementById('mat_creditos').value,
                    semestre: document.getElementById('mat_semestre').value,
                    carrera_codigo: "ICC",
                    carrera_nombre: "Ingeniería en Ciencias de la Computación",
                    profesor_id: document.getElementById('mat_profesor_id').value.trim(),
                    profesor_nombre: document.getElementById('mat_profesor_nombre').value.trim(),
                    prerrequisitos: prerrequisitos
                };

                const resp = await fetch('/api/materias', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });
                const data = await resp.json();
                if (resp.ok) {
                    window.location.reload();
                } else {
                    alert(data.error || 'Error de validación al guardar materia');
                }
            }

            async function actualizarMateria(e) {
                e.preventDefault();
                const id = document.getElementById('edit_mat_id').value;
                const payload = {
                    nombre: document.getElementById('edit_mat_nombre').value.trim(),
                    creditos: document.getElementById('edit_mat_creditos').value,
                    prerrequisito: document.getElementById('edit_mat_prerrequisito').value.trim()
                };

                const resp = await fetch('/api/materias/' + id, {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });
                const data = await resp.json();
                if (resp.ok) {
                    window.location.reload();
                } else {
                    alert(data.error || 'Error al actualizar materia');
                }
            }

            async function eliminarMateria(id) {
                if (!confirm('¿Deseas eliminar la materia ' + id + '?')) return;
                const resp = await fetch('/api/materias/' + id, { method: 'DELETE' });
                const data = await resp.json();
                if (resp.ok) {
                    window.location.reload();
                } else {
                    alert(data.error || 'Error al eliminar materia');
                }
            }

            // Cerrar al hacer clic en el overlay
            document.getElementById('modalNuevaMateria').addEventListener('click', function (e) {
                if (e.target === this) cerrarModalMateria();
            });
            document.getElementById('modalEditarMateria').addEventListener('click', function (e) {
                if (e.target === this) cerrarModalEditarMateria();
            });

            // Cerrar con Escape
            document.addEventListener('keydown', function (e) {
                if (e.key === 'Escape') {
                    cerrarModalMateria();
                    cerrarModalEditarMateria();
                }
            });
            //]]>
        </script>
    </xsl:template>
</xsl:stylesheet>