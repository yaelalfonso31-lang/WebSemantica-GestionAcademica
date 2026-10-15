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