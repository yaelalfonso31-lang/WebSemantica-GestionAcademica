from flask import Flask, session
import os

def create_app():
    # Inicializar la aplicación Flask
    app = Flask(__name__)
    
    # 1. Cargar configuración desde config.py en la raíz del proyecto
    app.config.from_object('config')
    if app.config.get('SECRET_KEY_ES_DE_DESARROLLO'):
        print("Advertencia: usando SECRET_KEY de desarrollo. Define la variable de entorno SECRET_KEY en producción.")

    # Asegurar que las carpetas de datos existan al arrancar
    os.makedirs(app.config.get('XML_DIR', 'data/xml'), exist_ok=True)
    os.makedirs(app.config.get('RDF_DIR', 'data/rdf'), exist_ok=True)

    with app.app_context():
        # 2. Inicializar y cargar el grafo RDF al arrancar
        # Importamos el servicio aquí para evitar dependencias circulares
        from app.services import rdf_graph
        try:
            # Supone que crearás una función cargar_grafo() en rdf_graph.py
            rdf_graph.cargar_grafo()
            print("Grafo RDF y ontología cargados correctamente en memoria.")
        except Exception as e:
            print(f"Advertencia: No se pudo cargar el grafo RDF inicial: {e}")

        # 3. Importar los Blueprints (módulos de rutas)
        # Autenticación
        from app.auth.routes import auth_bp
        
        # Vistas principales y utilidades
        from app.routes.dashboard import dashboard_bp
        from app.routes.kardex import kardex_bp
        from app.routes.horarios import horarios_bp
        from app.routes.calificaciones import calificaciones_bp
        from app.routes.consultas import consultas_bp
        
        # CRUD del catálogo
        from app.routes.alumnos import alumnos_bp
        from app.routes.profesores import profesores_bp
        from app.routes.materias import materias_bp
        from app.routes.carreras import carreras_bp
        from app.routes.grupos import grupos_bp

        # 4. Registrar los Blueprints en la aplicación principal
        app.register_blueprint(auth_bp)
        app.register_blueprint(dashboard_bp)
        app.register_blueprint(kardex_bp)
        app.register_blueprint(horarios_bp)
        app.register_blueprint(calificaciones_bp)
        app.register_blueprint(consultas_bp)
        app.register_blueprint(alumnos_bp)
        app.register_blueprint(profesores_bp)
        app.register_blueprint(materias_bp)
        app.register_blueprint(carreras_bp)
        app.register_blueprint(grupos_bp)

    # 5. Páginas de error con el mismo diseño del sistema (en lugar del HTML crudo de Flask)
    from app.services.transformer import transformar_a_html

    def _pagina_error(codigo, titulo, detalle):
        html = transformar_a_html(
            '<error/>', 'error.xsl',
            {'codigo': codigo, 'titulo': titulo, 'detalle': detalle,
             'rol_usuario': session.get('rol', 'visitante'),
             'nombre_usuario': session.get('nombre', 'Invitado')})
        return (html[0] if isinstance(html, tuple) else html), codigo

    @app.errorhandler(403)
    def _403(e):
        return _pagina_error(403, 'Acceso denegado', 'No tienes permiso para ver esta página.')

    @app.errorhandler(404)
    def _404(e):
        return _pagina_error(404, 'Página no encontrada', 'La dirección que buscas no existe o fue movida.')

    @app.errorhandler(500)
    def _500(e):
        return _pagina_error(500, 'Algo salió mal', 'Ocurrió un error inesperado. Ya quedó registrado en el servidor.')

    return app