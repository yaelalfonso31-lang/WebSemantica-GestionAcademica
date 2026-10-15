# app/auth/decorators.py
from functools import wraps
from flask import session, redirect, url_for, abort

def login_requerido(f):
    """Verifica que el usuario haya iniciado sesión antes de acceder a la ruta."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario_id' not in session:
            # Si no hay sesión, redirige a la ruta de login del blueprint auth
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def rol_requerido(*roles_permitidos):
    """Verifica que el rol almacenado en sesión coincida con los requeridos (ej. 'admin')."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            rol_actual = session.get('rol')
            if not rol_actual or rol_actual not in roles_permitidos:
                # Si el usuario no tiene el rol necesario, devuelve un error 403 (Forbidden)
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator