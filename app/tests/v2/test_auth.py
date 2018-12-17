"""
    app.tests.v2.auth
    ~~~~~~~~~~~~~~~~~~~
"""
from app import create_app
from instance.config import Config, TestConfig
from app.db import Model
from app.api.v2.models import Record, User, Blacklist
from datetime import datetime
import pytest
import json
from app.api.utils import make_token_header

@pytest.fixture
def client():
    """
    Configures the application for testing and initializes a new database.
    This fixture is called by each individual test.
    """
    app = create_app(TestConfig)
    # Configuration settings for tests
    app.config['JWT_SECRET_KEY'] = 'amsosecret'
    app.config['JWT_BLACKLIST_ENABLED'] = True
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
    app.config['PROPAGATE_EXCEPTIONS'] = True
    client = app.test_client()

    # Create an application context before running the tests
    ctx = app.app_context()
    ctx.push()

    Model.create_all_tables()

    yield client

    Model.clear_all_tables()
    ctx.pop()

#
# Test data
#

# Authentication
valid_signup_data_1 = {'username': 'arsene', 'password':'wenger'}
valid_signup_data_2 = {'username': 'shaka', 'password':'zuluzulu'}
invalid_username_1 = {'username': '', 'password':'secret'}
invalid_username_2 = {'username': '   ', 'password':'secret'}
invalid_username_3 = {'username': '1234', 'password':'secret'}
# Invalid password: too short (less than 5 characters)
invalid_password = {'username': 'arsene', 'password':'abc'}
duplicate_signup_data = {'username': 'arsene', 'password':'wenger'}


# Records
user_input = {'location': '-1.23, 36.5', 'comment':'crooked tendering processes'}


def test_authentication(client):
    """
    Tests for authentication endpoint
    """
    # SignUp Tests
    resp = client.post('/api/v2/auth/signup', data=valid_signup_data_1)
    assert resp.status_code == 201
    assert b'data'in resp.data
    assert b'status' in resp.data
    data = json.loads(resp.data.decode('utf-8'))
    data_dict = data['data'][0]
    assert 'access_token' in data_dict
    assert 'refresh_token' in data_dict
    # Invalid signup: either password or username are Invalid or missing
    resp = client.post('/api/v2/auth/signup', data=invalid_username_1)
    assert resp.status_code == 400
    resp = client.post('/api/v2/auth/signup', data=invalid_username_2)
    assert resp.status_code == 400
    resp = client.post('/api/v2/auth/signup', data=invalid_username_3)
    assert resp.status_code == 400
    resp = client.post('/api/v2/auth/signup', data=invalid_password)
    assert resp.status_code == 400
    resp = client.post('/api/v2/auth/signup')
    assert resp.status_code == 400
    # user already exists
    resp = client.post('/api/v2/auth/signup', data=duplicate_signup_data)
    assert resp.status_code == 400

    # Login Tests
    resp = client.post('/api/v2/auth/login', data=valid_signup_data_1)
    assert resp.status_code == 200
    data = json.loads(resp.data.decode('utf-8'))
    data_dict = data['data'][0]
    assert 'access_token' in data_dict
    assert 'refresh_token' in data_dict
    access_token = data_dict['access_token']
    refresh_token = data_dict['refresh_token']
    # Invalid login
    # password empty
    resp = client.post('/api/v2/auth/login', data={'username':'jambazi'})
    assert resp.status_code == 400
    # username empty
    resp = client.post('/api/v2/auth/login', data={'password':'wenger'})
    assert resp.status_code == 400
    # wrong credentials
    resp = client.post('/api/v2/auth/login', data=valid_signup_data_2)
    assert resp.status_code == 401
    # empty username and password
    resp = client.post('/api/v2/auth/login', data={'username':'', 'password':''})
    assert resp.status_code == 401

    # Refresh Tests
    # No authorization header
    resp = client.post('/api/v2/auth/refresh')
    assert resp.status_code == 401
    resp = client.post('/api/v2/auth/refresh', headers=make_token_header(access_token))
    assert resp.status_code == 422
    resp = client.post('/api/v2/auth/refresh', headers=make_token_header(refresh_token))
    assert resp.status_code == 200
    data = json.loads(resp.data.decode('utf-8'))
    data_dict = data['data'][0]
    assert 'access_token' in data_dict

    # Logout - acess token
    resp = client.delete('/api/v2/auth/logout')
    assert resp.status_code == 401
    resp = client.delete('/api/v2/auth/logout', headers=make_token_header(access_token))
    assert resp.status_code == 200
    resp = client.delete('/api/v2/auth/logout', headers=make_token_header(access_token))
    assert resp.status_code == 401
    resp = client.get('/api/v2/interventions', headers=make_token_header(access_token))
    assert resp.status_code == 401
    data = json.loads(resp.data.decode('utf-8'))
    assert 'revoked' in data['error']
    #
    # Logout - revoke token
    resp = client.delete('/api/v2/auth/refresh/logout', headers=make_token_header(access_token))
    assert resp.status_code == 422
    resp = client.delete('/api/v2/auth/refresh/logout', headers=make_token_header(refresh_token))
    assert resp.status_code == 200
    resp = client.delete('/api/v2/auth/refresh/logout', headers=make_token_header(refresh_token))
    assert resp.status_code == 401
    data = json.loads(resp.data.decode('utf-8'))
    assert 'revoked' in data['error']
