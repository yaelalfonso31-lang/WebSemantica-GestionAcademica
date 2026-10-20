from functools import wraps

from flask import flash, jsonify, redirect, request, session, url_for


def _es_api():
    return request.path.startswith('/api/') or request.is_json


def login_requerido(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            if _es_api():
                return jsonify({'error': 'Sesión expirada. Inicia sesión de nuevo.'}), 401
            flash('Por favor, inicia sesión para acceder a esta página.', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


def rol_requerido(*roles_permitidos):
    """Solo deja pasar a los roles indicados. Ej.: @rol_requerido('admin', 'profesor')"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if session.get('rol') not in roles_permitidos:
                if _es_api():
                    return jsonify({'error': 'No tienes permisos para esta operación.'}), 403
                flash('Acceso denegado: no tienes los permisos necesarios para ver esta sección.', 'danger')
                return redirect(url_for('dashboard.vista_dashboard'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator
