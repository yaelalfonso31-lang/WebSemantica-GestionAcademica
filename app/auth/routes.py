# app/auth/routes.py
from flask import Blueprint, flash, redirect, request, session, url_for

from app.services.security import verificar_contrasena
from app.services.transformer import transformar_a_html
from app.services.xml_utils import cargar, texto, xpath

auth_bp = Blueprint('auth', __name__)


def _buscar_usuario(username):
    # XPath con variable: el usuario escrito en el formulario nunca se concatena a la consulta
    encontrados = xpath(cargar('usuarios'), '//usuario[username=$u]', u=username)
    return encontrados[0] if encontrados else None


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = (request.form.get('username') or '').strip()
        password = request.form.get('password') or ''
        nodo = _buscar_usuario(username)

        if nodo is not None and verificar_contrasena(texto(nodo, 'password'), password):
            session.clear()  # evita reutilizar una sesión previa
            session.permanent = True
            session['user_id'] = nodo.get('id')
            session['username'] = texto(nodo, 'username', 'Usuario')
            session['nombre'] = texto(nodo, 'nombre', 'Sin Nombre')
            session['rol'] = texto(nodo, 'rol', 'visitante')
            # Vínculo con el registro real (alumno A006, profesor P012, ...)
            session['ref_id'] = texto(nodo, 'ref') or None

            if session['rol'] in ('alumno', 'profesor') and not session['ref_id']:
                flash('Tu cuenta aún no está vinculada a un registro de '
                      f"{session['rol']}. Pide al administrador que la asocie.", 'warning')
            return redirect(url_for('dashboard.vista_dashboard'))

        flash('Credenciales incorrectas. Verifica tu usuario y contraseña.', 'danger')

    if 'user_id' in session and request.method == 'GET':
        return redirect(url_for('dashboard.vista_dashboard'))
    return transformar_a_html('<login></login>', 'login.xsl')


@auth_bp.route('/logout')
def logout():
    """Limpia los datos de la sesión y devuelve al usuario a la vista de login."""
    session.clear()
    return redirect(url_for('auth.login'))
