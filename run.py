# run.py

from app import create_app

# Crea la instancia de la aplicación Flask utilizando la fábrica
app = create_app()

if __name__ == '__main__':
    # Ejecuta el servidor de desarrollo de Flask
    # debug=True reiniciará el servidor automáticamente si haces cambios en el código
    app.run(debug=True, host='127.0.0.1', port=5000)