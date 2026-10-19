// app/static/js/app.js

// Funciones para el Módulo de Alumnos
function eliminarAlumno(alumnoId) {
    if (confirm('¿Estás seguro de que deseas dar de baja y eliminar a este alumno del sistema?')) {
        fetch('/api/alumnos/' + alumnoId, { method: 'DELETE' })
            .then(response => response.json())
            .then(data => {
                if (data.error) alert('Error: ' + data.error);
                else {
                    alert(data.mensaje);
                    window.location.reload();
                }
            })
            .catch(error => console.error('Error:', error));
    }
}

function abrirModal() {
    const modal = document.getElementById('modalNuevoAlumno');
    if (modal) {
        modal.classList.remove('hidden');
        document.body.style.overflow = 'hidden';
    }
}


function cerrarModal() {
    const modal = document.getElementById('modalNuevoAlumno');

    if (modal && !modal.classList.contains('hidden')) {
        modal.classList.add('hidden');
        document.body.style.overflow = '';
    }
}

function guardarAlumno(event) {
    event.preventDefault();

    const form = document.getElementById('formNuevoAlumno');
    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());

    data.semestre = parseInt(data.semestre);
    data.promedio = parseFloat(data.promedio);

    fetch('/api/alumnos', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    })
        .then(response => response.json())
        .then(res => {
            if (res.error) {
                alert('⚠️ Error de Validación (XSD/DTD):\n\n' + res.error);
            } else {
                alert('✅ ' + res.mensaje);
                cerrarModal();
                window.location.reload();
            }
        })
        .catch(error => {
            alert('Error de conexión con el servidor.');
            console.error('Error:', error);
        });

    cerrarModal();
}

// Aquí Eduardo y Rubi agregar sus funciones:
// function guardarProfesor(event) { ... }
// function guardarMateria(event) { ... }


/* =========================================
   MÓDULO DE PROFESORES
   ========================================= */

// Abrir el modal de registro
function abrirModalProfesor() {
    const modal = document.getElementById('modalProfesor');
    const form = document.getElementById('formProfesor');

    if (!modal || !form) {
        console.error('No se encontró el modal o formulario de Profesores.');
        alert('Falta agregar el modal de Profesores al XSLT.');
        return;
    }

    form.reset();

    const idInput = form.elements.namedItem('id');
    if (idInput) {
        idInput.readOnly = false;
    }

    modal.classList.remove('hidden');
}

// Cerrar el modal
function cerrarModalProfesor() {
    const modal = document.getElementById('modalProfesor');
    const form = document.getElementById('formProfesor');

    if (modal) modal.classList.add('hidden');
    if (form) form.reset();

    const idInput = form?.elements.namedItem('id');
    if (idInput) idInput.readOnly = false;

    const titulo = document.getElementById('tituloModalProfesor');
    if (titulo) titulo.textContent = 'Registrar profesor';

    const boton = document.getElementById('botonGuardarProfesor');
    if (boton) boton.textContent = 'Guardar profesor';

    const metodo = document.getElementById('metodoProfesor');
    if (metodo) metodo.value = 'POST';
}

// ==========================================
// Módulo de Buscador SPARQL
// ==========================================
function lanzarConsultaSPARQL() {
    const archivoSeleccionado = document.getElementById('selectConsulta').value;

    if (!archivoSeleccionado) {
        alert("⚠️ Por favor selecciona una consulta del menú desplegable.");
        return;
    }

    // Efectos de carga visual
    document.getElementById('spinnerCarga').classList.remove('d-none');
    document.getElementById('headSPARQL').innerHTML = '';
    document.getElementById('bodySPARQL').innerHTML = '<tr><td class="text-center py-5 text-muted">Consultando el Grafo RDF...</td></tr>';
    document.getElementById('panelMetricas').classList.add('d-none');

    fetch('/api/consultas/ejecutar', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ archivo: archivoSeleccionado })
    })
        .then(response => response.json())
        .then(res => {
            document.getElementById('spinnerCarga').classList.add('d-none');

            if (res.error) {
                document.getElementById('bodySPARQL').innerHTML = `<tr><td class="text-center py-5 text-danger fw-bold">❌ Error SPARQL: ${res.error}</td></tr>`;
                return;
            }

            // Mostrar métricas
            document.getElementById('panelMetricas').classList.remove('d-none');
            document.getElementById('totalResultados').innerText = res.total_resultados;

            const data = res.data;
            const thead = document.getElementById('headSPARQL');
            const tbody = document.getElementById('bodySPARQL');

            thead.innerHTML = '';
            tbody.innerHTML = '';

            if (data.length === 0) {
                thead.innerHTML = '<tr><th class="py-3 px-4">Resultado</th></tr>';
                tbody.innerHTML = '<tr><td class="text-center py-5 text-muted">No se encontraron inferencias para esta consulta.</td></tr>';
                return;
            }

            // 1. Generar los encabezados <th> leyendo las llaves del primer diccionario (las variables ?x del SELECT)
            let trHead = document.createElement('tr');
            const columnas = Object.keys(data[0]);
            columnas.forEach(col => {
                let th = document.createElement('th');
                th.className = "px-4 text-capitalize";
                th.innerText = col;
                trHead.appendChild(th);
            });
            thead.appendChild(trHead);

            // 2. Generar las filas <td> con los valores devueltos
            data.forEach(fila => {
                let trBody = document.createElement('tr');
                columnas.forEach(col => {
                    let td = document.createElement('td');
                    td.className = "px-4";

                    // Formateo visual: Si detecta una URL/URI, le da estilo de etiqueta
                    let valor = fila[col];
                    if (valor.includes("http://")) {
                        valor = `<span class="badge bg-secondary badge-mono" title="${valor}">` + valor.split('/').pop().split('#').pop() + `</span>`;
                        td.innerHTML = valor;
                    } else {
                        td.innerText = valor;
                    }

                    trBody.appendChild(td);
                });
                tbody.appendChild(trBody);
            });
        })
        .catch(error => {
            document.getElementById('spinnerCarga').classList.add('d-none');
            document.getElementById('bodySPARQL').innerHTML = `<tr><td class="text-center py-5 text-danger fw-bold">Error de red al consultar el motor.</td></tr>`;
            console.error('Error:', error);
        });
}


function obtenerDatosFormularioProfesor(form) {
    const datos = Object.fromEntries(new FormData(form).entries());

    const textoMaterias = datos.materias || '';
    delete datos.materias;

    datos.materias_impartidas = textoMaterias
        .split('\n')
        .map(linea => linea.trim())
        .filter(Boolean)
        .map(linea => {
            const separador = linea.indexOf('|');

            if (separador === -1) {
                throw new Error(
                    'Cada materia debe tener el formato CODIGO|Nombre. Ejemplo: CS201|Programación'
                );
            }

            const codigo = linea.slice(0, separador).trim();
            const nombre = linea.slice(separador + 1).trim();

            if (!codigo || !nombre) {
                throw new Error(
                    'Cada materia debe incluir su código y su nombre.'
                );
            }

            return { codigo, nombre };
        });

    return datos;
}



// Registrar o actualizar un profesor
async function guardarProfesor(event) {
    event.preventDefault();

    const form = document.getElementById('formProfesor');
    if (!form) return;

    try {
        const datos = obtenerDatosFormularioProfesor(form);
        const metodoInput = document.getElementById('metodoProfesor');
        const metodo = metodoInput?.value || 'POST';

        const profesorId = datos.id;

        const url = metodo === 'PUT'
            ? '/api/profesores/' + encodeURIComponent(profesorId)
            : '/api/profesores';

        const response = await fetch(url, {
            method: metodo,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(datos)
        });

        const resultado = await response.json();

        if (!response.ok) {
            alert(
                'No se pudo guardar el profesor:\n' +
                (resultado.error || 'Error inesperado') +
                (resultado.detalle ? '\n' + resultado.detalle : '')
            );
            return;
        }

        alert(resultado.mensaje || 'Operación realizada correctamente.');
        cerrarModalProfesor();
        window.location.reload();

    } catch (error) {
        alert(error.message || 'Error de conexión con el servidor.');
        console.error('Error al guardar profesor:', error);
    }
}

// Consultar los datos y abrir el modal en modo edición
async function editarProfesor(profesorId) {
    try {
        const response = await fetch(
            '/api/profesores/' + encodeURIComponent(profesorId)
        );

        const profesor = await response.json();

        if (!response.ok) {
            alert(profesor.error || 'No se pudo consultar el profesor.');
            return;
        }

        const modal = document.getElementById('modalProfesor');
        const form = document.getElementById('formProfesor');

        if (!modal || !form) {
            alert('Falta agregar el modal de Profesores al XSLT.');
            return;
        }

        form.reset();

        // Rellenar los campos que existan en el formulario.
        for (const campo of [
            'id', 'nombre', 'especialidad', 'correo', 'departamento'
        ]) {
            const input = form.elements.namedItem(campo);
            if (input && profesor[campo] != null) {
                input.value = profesor[campo];
            }
        }

        // Mostrar las materias en formato CODIGO|Nombre.  
        const campoMaterias = form.elements.namedItem('materias');

        if (campoMaterias) {
            const materias = profesor.materias_impartidas || [];

            campoMaterias.value = materias
                .map(materia => `${materia.codigo || ''}|${materia.nombre || ''}`)
                .join('\n');
        }

        const idInput = form.elements.namedItem('id');
        if (idInput) idInput.readOnly = true;

        const titulo = document.getElementById('tituloModalProfesor');
        if (titulo) titulo.textContent = 'Editar profesor';

        const boton = document.getElementById('botonGuardarProfesor');
        if (boton) boton.textContent = 'Guardar cambios';

        const metodo = document.getElementById('metodoProfesor');
        if (metodo) metodo.value = 'PUT';

        modal.classList.remove('hidden');

    } catch (error) {
        console.error('Error al consultar profesor:', error);
        alert('No se pudo conectar con el servidor.');
    }
}

// Eliminar un profesor
async function eliminarProfesor(profesorId) {
    if (!confirm(
        '¿Estás seguro de que deseas eliminar al profesor ' +
        profesorId + '?'
    )) {
        return;
    }

    try {
        const response = await fetch(
            '/api/profesores/' + encodeURIComponent(profesorId),
            { method: 'DELETE' }
        );

        const resultado = await response.json();

        if (!response.ok) {
            alert(resultado.error || 'No se pudo eliminar el profesor.');
            return;
        }

        alert(resultado.mensaje || 'Profesor eliminado correctamente.');
        window.location.reload();

    } catch (error) {
        console.error('Error al eliminar profesor:', error);
        alert('Error de conexión con el servidor.');
    }
}

// Variable global para controlar el modal de Bootstrap
let modalEditar;

function abrirModalEditarAlumno(id, matricula, nombre, apellidos, correo, carrera, semestre, promedio, estatus) {
    // Llenar los campos del formulario
    document.getElementById('edit_id').value = id;
    document.getElementById('edit_matricula').value = matricula;
    document.getElementById('edit_nombre').value = nombre;
    document.getElementById('edit_apellidos').value = apellidos;
    document.getElementById('edit_correo').value = correo;
    document.getElementById('edit_carrera').value = carrera;
    document.getElementById('edit_semestre').value = semestre;
    document.getElementById('edit_promedio').value = promedio;
    document.getElementById('edit_estatus').value = estatus;

    // Mostrar el modal usando la API de Bootstrap
    const modal = document.getElementById('modalEditarAlumno');
    if (modal) {
        modal.classList.remove('hidden');
        document.body.style.overflow = 'hidden'; // bloquear scroll del body
    }
}

function cerrarModalEditar() {
    const modal = document.getElementById('modalEditarAlumno');
    if (modal) {
        modal.classList.add('hidden');
        document.body.style.overflow = '';
    }
}

function actualizarAlumno(event) {
    event.preventDefault();

    const id = document.getElementById('edit_id').value;
    const datos = {
        matricula: document.getElementById('edit_matricula').value,
        nombre: document.getElementById('edit_nombre').value,
        apellidos: document.getElementById('edit_apellidos').value,
        correo: document.getElementById('edit_correo').value,
        carrera_id: document.getElementById('edit_carrera').value,
        semestre: document.getElementById('edit_semestre').value,
        promedio: document.getElementById('edit_promedio').value,
        estatus: document.getElementById('edit_estatus').value
    };

    fetch('/api/alumnos/' + id, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(datos)
    })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert('Error: ' + data.error);
            } else {
                alert('✅ ' + data.mensaje);
                modalEditar.hide();
                window.location.reload();
            }
        })
        .catch(error => console.error('Error:', error));
}

// ==========================================
// Módulo de Materias
// ==========================================
let modalEditarMateria;

function abrirModalEditarMateria(id, nombre, creditos, prerrequisito) {
    document.getElementById('edit_mat_id').value = id;
    document.getElementById('edit_mat_nombre').value = nombre;
    document.getElementById('edit_mat_creditos').value = creditos;
    document.getElementById('edit_mat_prerrequisito').value = prerrequisito || '';

    document.getElementById('modalEditarMateria').classList.remove('hidden');
    document.body.classList.add('modal-open');
}

function cerrarModalEditarMateria() {
    document.getElementById('modalEditarMateria').classList.add('hidden');
    document.body.classList.remove('modal-open');
}

function actualizarMateria(event) {
    event.preventDefault();

    const id = document.getElementById('edit_mat_id').value;
    const datos = {
        nombre: document.getElementById('edit_mat_nombre').value,
        creditos: document.getElementById('edit_mat_creditos').value,
        prerrequisito: document.getElementById('edit_mat_prerrequisito').value
    };

    fetch('/api/materias/' + id, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(datos)
    })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert('Error: ' + data.error);
            } else {
                alert('✅ ' + data.mensaje);
                modalEditarMateria.hide();
                window.location.reload();
            }
        })
        .catch(error => console.error('Error:', error));
}