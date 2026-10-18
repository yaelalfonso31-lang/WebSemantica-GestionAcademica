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
    document.getElementById('modalNuevoAlumno').classList.remove('hidden');
}

function cerrarModal() {
    document.getElementById('modalNuevoAlumno').classList.add('hidden');
    document.getElementById('formNuevoAlumno').reset();
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

// Leer el formulario y convertir las materias en una lista.
// Formato esperado por línea del campo "materias":
// MAT001|Programación
// MAT002|Bases de datos


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
