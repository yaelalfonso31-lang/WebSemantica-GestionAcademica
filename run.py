# run.py
import os

from app import create_app

app = create_app()

if __name__ == '__main__':
    # debug solo si lo pides: FLASK_DEBUG=1 python run.py (nunca en producción)
    app.run(debug=os.environ.get('FLASK_DEBUG') == '1', host='127.0.0.1', port=5000)
