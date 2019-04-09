"""
    tests.v2.auth
    ~~~~~~~~~~~~~~~~~~~
"""
from app import create_app
from instance.config import TestConfig
import pytest
from app.api.utils import make_token_header
from app.db import Model



@pytest.fixture
def app():

    app = create_app(TestConfig)
   
    with app.app_context():

        Model.create_all_tables()

    yield app

    Model.clear_all_tables()

    

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username='test', password='test'):
        return self._client.post(
                '/auth/login',
                data={'username': username, 'password': password}
                )

    def logout(self):
        return self._client.get('/auth/logout')

@pytest.fixture
def auth(client):
    return AuthActions(client)
