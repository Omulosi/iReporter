"""
    tests.v2.users
    ~~~~~~~~~~~~~~~~~~~~~~

    Tests for users resources
"""

import json
from app.helpers import make_token_header
from app.models import User


def test_get_user(client, auth):
    """
    Tests endpoint for getting user info
    """
    #:  No authorization header: should return an unauthorized error
    resp = client.get('/api/v2/user')
    assert resp.status_code == 401

    #: Sign in and acquire tokens
    resp = auth.login()
    data = json.loads(resp.data.decode('utf-8'))['data'][0]
    access_token = data['access_token']

    resp = client.get('/api/v2/user', headers=make_token_header(access_token))
    assert resp.status_code == 200
    data = json.loads(resp.data.decode('utf-8'))
    assert len(data['data']) == 1

def test_get_all_users(client, auth):
    """
    Tests endpoint for getting user info
    """
    #:  No authorization header: should return an unauthorized error
    resp = client.get('/api/v2/users')
    assert resp.status_code == 401


    #: create users

    resp = auth.signup(username='patrice', password='lumumba')
    data = json.loads(resp.data.decode('utf-8'))['data'][0]
    access_token_1 = data['access_token']

    resp = auth.signup(username='thomas', password='sankara',)
    data = json.loads(resp.data.decode('utf-8'))['data'][0]
    access_token_2 = data['access_token']

    #: create admin user
    resp = auth.signup(username='mahatma', password='gandhi', admin=True)
    data = json.loads(resp.data.decode('utf-8'))['data'][0]
    access_token_admin = data['access_token']
 
    #: Only admin can access this endpoint
    resp = client.get('/api/v2/users', headers=make_token_header(access_token_1))
    assert resp.status_code == 403

    resp = client.get('/api/v2/users', headers=make_token_header(access_token_admin))
    assert resp.status_code == 200
    data = json.loads(resp.data.decode('utf-8'))
    print(data)
    assert len(data['data']) == 4