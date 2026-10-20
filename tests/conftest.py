import os
import shutil
import sys

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)


@pytest.fixture
def app(tmp_path):
    """App con una COPIA de data/ y de los demás recursos: los tests nunca tocan tus datos reales."""
    from app import create_app
    from app.services.rdf_graph import SemanticEngine

    datos = tmp_path / 'data'
    shutil.copytree(os.path.join(ROOT, 'data'), datos)
    app = create_app()
    app.config.update(TESTING=True, XML_DIR=str(datos / 'xml'), RDF_DIR=str(datos / 'rdf'),
                      BACKUP_DIR=str(datos / 'backups'))
    SemanticEngine._grafo_memoria = None
    yield app
    SemanticEngine._grafo_memoria = None


@pytest.fixture
def cliente(app):
    return app.test_client()


def entrar(cliente, usuario, password='1234'):
    cliente.get('/logout')
    return cliente.post('/login', data={'username': usuario, 'password': password})
