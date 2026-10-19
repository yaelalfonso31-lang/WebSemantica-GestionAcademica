# app/auth/routes.py
import os
from config import XML_DIR
from lxml import etree
from flask import Blueprint, request, session, redirect, url_for, flash, current_app
from app.services.security import verificar_contrasena
from app.services.transformer import transformar_a_html

# Se define el blueprint para las rutas de autenticación
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # 1. Obtener datos del formulario HTML
        username_input = request.form.get('username')
        password_input = request.form.get('password')
        
        # 2. Cargar el XML de usuarios
        usuarios_path = os.path.join(current_app.config.get('XML_DIR', 'data/xml'), 'usuarios.xml')
        
        if os.path.exists(usuarios_path):
            tree = etree.parse(usuarios_path)
            
            # 3. Buscar coincidencia exacta usando XPath
            # Esto busca un <usuario> cuyos hijos <username> y <password> coincidan con lo ingresado
            usuario_nodo = tree.xpath(f"//usuario[username='{username_input}' and password='{password_input}']")
            
            if usuario_nodo:
                nodo = usuario_nodo[0]
                # 4. Inyectar datos en la sesión activa
                session['user_id'] = nodo.get('id')
                # Usamos findtext() para leer el contenido de las etiquetas hijas de forma segura
                session['username'] = nodo.findtext('username', default='Usuario')
                session['nombre'] = nodo.findtext('nombre', default='Sin Nombre')
                session['rol'] = nodo.findtext('rol', default='visitante')
                
                # 5. Redireccionar al enrutador de roles
                return redirect(url_for('dashboard.vista_dashboard'))
            else:
                flash('Credenciales incorrectas. Verifica tu usuario y contraseña.', 'danger')
        else:
            flash('Error del sistema: Base de datos de usuarios no encontrada.', 'danger')

    # Si la petición es GET o las credenciales fallaron, renderiza el formulario
    return transformar_a_html(
        xml_path_or_string='<login></login>', 
        xslt_filename='login.xsl'
    )

@auth_bp.route('/logout')
def logout():
    """Limpia los datos de la sesión y devuelve al usuario a la vista de login."""
    session.clear()
    return redirect(url_for('auth.login'))