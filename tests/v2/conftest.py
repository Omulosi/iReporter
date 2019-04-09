"""
    tests.v2.auth
    ~~~~~~~~~~~~~~~~~~~
"""

import json
from app import create_app
from instance.config import TestConfig
import pytest
from app.api.utils import make_token_header
from app.api.v2.models import User
from app.db import Model



@pytest.fixture
def app():

    app = create_app(TestConfig)
   
    with app.app_context():

        Model.create_all_tables()

        user = User(username='test', password='test-password')
        user.put()
       
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

    def signup(self, username, password):
        return self._client.post(
                '/api/v2/auth/signup',
                data={'username': username, 'password': password}
                )

    def login(self, username='test', password='test-password'):
        return self._client.post(
                '/api/v2/auth/login',
                data={'username': username, 'password': password}
                )

    def logout(self, token, refresh=False, access=False):
        if refresh:
            return self._client.delete(
                '/api/v2/auth/refresh/logout',
                headers=make_token_header(token))
        if access:
           return self._client.delete(
               '/api/v2/auth/logout',
               headers=make_token_header(token))

@pytest.fixture
def auth(client):
    return AuthActions(client)
