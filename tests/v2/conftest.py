"""
    tests.v2.auth
    ~~~~~~~~~~~~~~

    This module contains functions for configuring the application
    for testing
"""

import json
from app import create_app
from config import TestConfig
import pytest
from app.helpers import make_token_header
from app.models import User, Model, Record
from app.db import db


@pytest.fixture
def app():

    app = create_app(TestConfig)
   
    with app.app_context():

        db.init_db()
        
        USER = User()
        USER.add(username='test', password='test-password')
       
        yield app

        db.clear_tables() 

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def signup(self, username, password, admin=False):
        return self._client.post(
                '/api/v2/auth/signup',
                data={'username': username, 'password': password, 'isadmin': admin}
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
