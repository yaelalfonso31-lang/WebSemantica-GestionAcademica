from werkzeug.security import check_password_hash, generate_password_hash


def hashear_contrasena(password):
    """Devuelve el hash que se guarda en usuarios.xml (nunca la contraseña en claro)."""
    return generate_password_hash(password)


def verificar_contrasena(hash_guardado, password_ingresado):
    """True si la contraseña ingresada corresponde al hash guardado."""
    if not hash_guardado or not password_ingresado:
        return False
    try:
        return check_password_hash(hash_guardado, password_ingresado)
    except ValueError:  # hash malformado / texto plano heredado
        return False
