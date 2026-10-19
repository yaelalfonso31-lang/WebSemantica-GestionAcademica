from functools import wraps
from flask import session, redirect, url_for, flash

def login_requerido(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Por favor, inicia sesión para acceder a esta página.', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def rol_requerido(*roles_permitidos):
    """
    Decorador que verifica si el rol de la sesión actual está en la lista de roles permitidos.
    Ejemplo de uso: @rol_requerido('admin', 'profesor')
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            rol_actual = session.get('rol')
            if rol_actual not in roles_permitidos:
                flash('Acceso denegado: No tienes los permisos necesarios para ver esta sección.', 'danger')
                return redirect(url_for('dashboard.vista_dashboard'))
            return f(*args, **kwargs)
        return decorated_function   
    return decorator