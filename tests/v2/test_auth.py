"""
    app.tests.v2.auth
    ~~~~~~~~~~~~~~~~~~~
"""

from app.api.v2.models import Record, User, Blacklist
from datetime import datetime
import pytest
import json
from app.helpers import make_token_header


def test_register(client):
     # SignUp Tests
    resp = client.post('/api/v2/auth/signup', 
                        data={'username': 'test2', 'password':'test-password-2'})
    assert resp.status_code == 201
    #: check that reponse object has 'data' and 'status' fields
    assert b'data'in resp.data
    assert b'status' in resp.data
    #: check for presence of access and refresh tokens
    data = json.loads(resp.data.decode('utf-8'))
    data_dict = data['data'][0]
    assert 'access_token' in data_dict
    assert 'refresh_token' in data_dict


@pytest.mark.parametrize(('username','password'), (
    ('', 'secret'),
    ('', ''),
    ('   ', 'secret'),
    ('1234', 'secret'),
    ('arsene', 'abc'),
    ('   ', '   '),
    ))
def test_register_validate_input(client, username, password):
    # Sing up with invalid data
    resp = client.post(
            '/api/v2/auth/signup',
            data={'username': username, 'password': password}
            )
    assert resp.status_code == 400


def test_login(client, auth):
    #: Login Tests
    resp = auth.login()
    assert resp.status_code == 200
    data = json.loads(resp.data.decode('utf-8'))
    data_dict = data['data'][0]
    assert 'access_token' in data_dict
    assert 'refresh_token' in data_dict

@pytest.mark.parametrize(('username','password', 'error_code'), (
    (None, 'test-password', 400),
    ('test', None, 400),
    (None, None, 400),
    ('   ', 'test-password', 401),
    ('1234', 'secret', 401),
    ('test', 'abc', 401),
    ('nero', 'augustus', 401),
    ))
def test_login_validate_input(client, auth, username, password, error_code):
    #: Invalid login data
    resp = auth.login(username=username, password=password)
    print(resp.data)
    assert resp.status_code == error_code


def test_refresh(client, auth):
    resp = auth.login()
    data = json.loads(resp.data.decode('utf-8'))['data'][0]
    access_token, refresh_token = data['access_token'], data['refresh_token']

    #: successful response returns a refresh token
    resp = client.post('/api/v2/auth/refresh', headers=make_token_header(refresh_token))
    assert resp.status_code == 200
    data = json.loads(resp.data.decode('utf-8'))
    data_dict = data['data'][0]
    assert 'access_token' in data_dict

def test_refresh_validate_header(client, auth):
    #: login to obtain access and refresh tokens
    resp = auth.login()
    data = json.loads(resp.data.decode('utf-8'))['data'][0]
    access_token, refresh_token = data['access_token'], data['refresh_token']

    resp = client.post('/api/v2/auth/refresh')
    #: No authorization header
    assert resp.status_code == 401
    #: Only refresh tokens allowed
    resp = client.post('/api/v2/auth/refresh', headers=make_token_header(access_token))
    assert resp.status_code == 422


def test_logout(client, auth):
    resp = auth.login()
    data = json.loads(resp.data.decode('utf-8'))['data'][0]
    access_token, refresh_token = data['access_token'], data['refresh_token']

    #: Log out using access token
    resp = client.delete('/api/v2/auth/logout', headers=make_token_header(access_token))
    assert resp.status_code == 200

    #: Log out using refresh token
    resp = client.delete('/api/v2/auth/refresh/logout', headers=make_token_header(refresh_token))
    assert resp.status_code == 200

def test_logout_validate_input(client, auth):
    resp = auth.login()
    data = json.loads(resp.data.decode('utf-8'))['data'][0]
    access_token, refresh_token = data['access_token'], data['refresh_token']

    #: No token provided
    resp = client.delete('/api/v2/auth/logout')
    assert resp.status_code == 401
    resp = client.delete('/api/v2/auth/refresh/logout')
    assert resp.status_code == 401

    #: Log out with invalid token
    resp = auth.logout(access_token, refresh=True) # using access token on refresh logout link
    assert resp.status_code == 422
    resp = auth.logout(refresh_token, access=True) # using refresh token on access logout link
    assert resp.status_code == 422

    #: Log out with revoked access token
    resp = auth.logout(access_token, access=True) # first revoke token
    resp = auth.logout(access_token, access=True)
    assert resp.status_code == 401
    assert b"Token has been revoked" in resp.data

    #: Logout with revoked refresh token
    resp = auth.logout(refresh_token, refresh=True) # first revoke token
    resp = auth.logout(refresh_token, refresh=True)
    assert resp.status_code == 401
    assert b"Token has been revoked" in resp.data
