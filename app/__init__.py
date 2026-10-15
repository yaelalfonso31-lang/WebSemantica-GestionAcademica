from flask import Flask
import os

def create_app():
    # Inicializar la aplicación Flask
    app = Flask(__name__)
    
    # 1. Cargar configuración desde config.py en la raíz del proyecto
    app.config.from_object('config')

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

    return app