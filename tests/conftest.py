import os
import shutil
import sys

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

FIXTURES = os.path.join(ROOT, 'tests', 'fixtures')


@pytest.fixture
def app(tmp_path, monkeypatch):
    """App con una COPIA de los datos de tests/fixtures: nunca toca tu data/ real ni cambia con ella."""
    import config
    from app import create_app
    from app.services.rdf_graph import SemanticEngine

    datos = tmp_path / 'data'
    shutil.copytree(os.path.join(FIXTURES, 'xml'), datos / 'xml')
    os.makedirs(datos / 'rdf'); os.makedirs(datos / 'backups')
    for clave, sub in (('XML_DIR', 'xml'), ('RDF_DIR', 'rdf'), ('BACKUP_DIR', 'backups')):
        monkeypatch.setattr(config, clave, str(datos / sub))
    SemanticEngine._grafo_memoria = None
    app = create_app()
    app.config.update(TESTING=True)
    yield app
    SemanticEngine._grafo_memoria = None


@pytest.fixture
def cliente(app):
    return app.test_client()


def entrar(cliente, usuario, password='1234'):
    cliente.get('/logout')
    return cliente.post('/login', data={'username': usuario, 'password': password})
