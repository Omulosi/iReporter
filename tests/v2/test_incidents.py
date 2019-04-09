"""
    app.tests.v2.incidents
    ~~~~~~~~~~~~~~~~~~~~~~
"""
import json
import pytest
from app.api.utils import make_token_header
from app.api.v2.models import User


#
# Test data
#

user_input = {'location': '-1.23, 36.5', 'comment':'crooked tendering processes'}
valid_signup_data_1 = {'username': 'arsene', 'password':'wengerin'}
valid_signup_data_2 = {'username': 'patrice', 'password':'lumumba'}
valid_admin_data = {'username': 'aluta', 'password':'continua', 'isadmin':True}

def test_get_all_incidences(client):
    """
    Tests endpoint for getting all incidences
    """
    # No authorization header: should return an unauthorized error
    resp = client.get('/api/v2/interventions')
    assert resp.status_code == 401
    # get tokens
    resp = client.post('/api/v2/auth/signup', data=valid_signup_data_2)
    assert resp.status_code == 201
    data = json.loads(resp.data.decode('utf-8'))
    data_dict = data['data'][0]
    access_token = data_dict['access_token']
    refresh_token = data_dict['refresh_token']
    # Initial Request: No data
    resp = client.get('/api/v2/interventions', headers=make_token_header(access_token))
    assert resp.status_code == 200
    data = json.loads(resp.data.decode('utf-8'))
    assert len(data['data']) == 0
    # Valid input data
    resp = client.post('/api/v2/interventions', data=user_input, headers=make_token_header(access_token))
    assert resp.status_code == 201
    # Check that the data was added
    resp = client.get('/api/v2/interventions', headers=make_token_header(access_token))
    assert resp.status_code == 200
    assert b'data'in resp.data
    assert b'status' in resp.data
    data = json.loads(resp.data.decode('utf-8'))
    assert 'id' in data['data'][0]

def test_post_incident(client):
    """
    Tests the create red-flag endpoint
    """
    resp = client.post('/api/v2/interventions', data=user_input)
    assert resp.status_code == 401
    # Obtain tokens
    resp = client.post('/api/v2/auth/signup', data=valid_signup_data_2)
    assert resp.status_code == 201
    data = json.loads(resp.data.decode('utf-8'))
    data_dict = data['data'][0]
    access_token = data_dict['access_token']
    refresh_token = data_dict['refresh_token']
    # create record
    resp = client.post('/api/v2/interventions', data=user_input, headers=make_token_header(access_token))
    assert resp.status_code == 201
    data = json.loads(resp.data.decode('utf-8'))
    data = data['data'][0]
    assert resp.mimetype == 'application/json'
    assert resp.headers['Location'] is not None
    #
    # Invald requests
    # only access tokens allowed
    resp = client.post('/api/v2/interventions', data=user_input, headers=make_token_header(refresh_token))
    assert resp.status_code == 422
    resp = client.post('/api/v2/interventions', data={'location': '23,53'}, headers=make_token_header(access_token))
    assert resp.status_code ==  400
    resp = client.post('/api/v2/interventions', data={'comment': 'thief'}, headers=make_token_header(access_token))
    assert resp.status_code ==  400
    resp = client.post('/api/v2/interventions', data=None, headers=make_token_header(access_token))
    assert resp.status_code ==  400
    # input data should not be blank
    resp = client.post('/api/v2/interventions', data={'location': '', 'comment':''}, headers=make_token_header(access_token))
    assert resp.status_code ==  400
    resp = client.post('/api/v2/interventions', data={'location': '     ', 'comment':'      '}, headers=make_token_header(access_token))
    assert resp.status_code ==  400
    # test location
    resp = client.post('/api/v2/interventions', data={'location': '93,23'}, headers=make_token_header(access_token))
    assert resp.status_code ==  400
    resp = client.post('/api/v2/interventions', data={'location': '-91,23'}, headers=make_token_header(access_token))
    assert resp.status_code ==  400
    resp = client.post('/api/v2/interventions', data={'location': '34,181'}, headers=make_token_header(access_token))
    assert resp.status_code ==  400
    resp = client.post('/api/v2/interventions', data={'location': '45,-183'}, headers=make_token_header(access_token))
    assert resp.status_code ==  400

def test_get_incident(client):
    # Obtain tokens
    resp = client.post('/api/v2/auth/signup', data=valid_signup_data_1)
    assert resp.status_code == 201
    data = json.loads(resp.data.decode('utf-8'))
    data_dict = data['data'][0]
    access_token = data_dict['access_token']
    refresh_token = data_dict['refresh_token']
    # create test data
    resp = client.post('/api/v2/interventions', data=user_input, headers=make_token_header(access_token))
    assert resp.status_code == 201
    data = json.loads(resp.data.decode('utf-8'))
    uri = data['uri']
    #
    resp = client.get(uri, headers=make_token_header(access_token))
    assert resp.status_code == 200
    data = json.loads(resp.data.decode('utf-8'))
    data = data['data']
    assert data['location']
    assert data['comment']
    assert ['type']
    assert ['status']
    assert ['createdBy']
    assert ['id']
    assert ['Images']
    assert ['Videos']
    # Invalid requests
    resp = client.get('/api/v1/interventions/999', headers=make_token_header(access_token))
    assert resp.status_code == 404
    resp = client.get('/api/v2/interventions/some-id', headers=make_token_header(access_token))
    assert resp.status_code == 404

    # Unauthorized access
    resp = client.post('/api/v2/interventions', data=user_input)
    assert resp.status_code == 401

def test_delete_incident(client):
    # Obtain tokens
    resp = client.post('/api/v2/auth/signup', data=valid_signup_data_1)
    assert resp.status_code == 201
    data = json.loads(resp.data.decode('utf-8'))
    data_dict = data['data'][0]
    access_token_1 = data_dict['access_token']
    refresh_token_1 = data_dict['refresh_token']
    # create test data
    resp = client.post('/api/v2/interventions', data=user_input, headers=make_token_header(access_token_1))
    assert resp.status_code == 201
    data = json.loads(resp.data.decode('utf-8'))
    uri = data['uri']
    # test delete
    resp = client.delete(uri, headers=make_token_header(access_token_1))
    assert resp.status_code  == 200
    assert b'data' in resp.data
    assert b'status' in  resp.data
    # check that deletion is successful
    resp = client.get(uri, headers=make_token_header(access_token_1))
    assert resp.status_code == 404
    # Unauthorized access
    resp = client.delete(uri)
    assert resp.status_code == 401
    # invalid ids
    resp = client.delete('/api/v2/interventions/9999', headers=make_token_header(access_token_1))
    assert resp.status_code == 404
    resp = client.delete('/api/v2/interventions/data-id', headers=make_token_header(access_token_1))
    assert resp.status_code == 404
    # only an access token can delete
    resp = client.delete('/api/v2/interventions/9999', headers=make_token_header(refresh_token_1))
    assert resp.status_code == 422
    #
    # A user can only delete own record
    # second user
    resp = client.post('/api/v2/auth/signup', data=valid_signup_data_2)
    assert resp.status_code == 201
    data = json.loads(resp.data.decode('utf-8'))
    data_dict = data['data'][0]
    access_token_2 = data_dict['access_token']
    #
    resp = client.post('/api/v2/interventions', data=user_input, headers=make_token_header(access_token_1))
    assert resp.status_code == 201
    data = json.loads(resp.data.decode('utf-8'))
    uri_1 = data['uri']
    resp = client.post('/api/v2/interventions', data=user_input, headers=make_token_header(access_token_2))
    assert resp.status_code == 201
    data = json.loads(resp.data.decode('utf-8'))
    uri_2 = data['uri']
    #
    resp = client.delete(uri_2, headers=make_token_header(access_token_1))
    assert resp.status_code == 403
    resp = client.delete(uri_1, headers=make_token_header(access_token_2))
    assert resp.status_code == 403

def test_patch_location_or_comment(client):
    # Obtain tokens
    resp = client.post('/api/v2/auth/signup', data=valid_signup_data_1)
    assert resp.status_code == 201
    data = json.loads(resp.data.decode('utf-8'))
    data_dict = data['data'][0]
    access_token_1 = data_dict['access_token']
    refresh_token_1 = data_dict['refresh_token']
    #
    resp = client.post('/api/v2/auth/signup', data=valid_signup_data_2)
    assert resp.status_code == 201
    data = json.loads(resp.data.decode('utf-8'))
    data_dict = data['data'][0]
    access_token_2 = data_dict['access_token']

    def update_field(field):
        # create the incident to use for testing updates
        resp = client.post('/api/v2/interventions', data=user_input, headers=make_token_header(access_token_1))
        assert resp.status_code == 201
        data = json.loads(resp.data.decode('utf-8'))
        uri_1 = data['uri'] + '/' + field

        # valid data
        if field == 'location':
            update = {'location': '-15.7, 77.2'}
        if field == 'comment':
            update = {'comment': 'lipa kama tender'}
        resp = client.patch(uri_1, data=update, headers=make_token_header(access_token_1))
        assert resp.status_code  == 200
        assert b'data' in resp.data
        assert b'status' in  resp.data
        #
        # Invalid IDs
        resp = client.patch('/api/v2/interventions/10000/' + field, headers=make_token_header(access_token_1))
        assert resp.status_code == 404
        resp = client.patch('/api/v2/interventions/record/' + field, headers=make_token_header(access_token_1))
        assert resp.status_code == 404
        #
        # Too many input fields
        resp = client.patch(uri_1, data={'location': '34,34', 'comment': 'corrupt lawyers'}, headers=make_token_header(access_token_1))
        assert resp.status_code == 400
        if field == 'location':
            # only location should be in input data
            resp = client.patch(uri_1, data={'comment': 'corrupt lawyers'}, headers=make_token_header(access_token_1))
            assert resp.status_code == 400
            # check for invalid location format
            resp = client.patch(uri_1, data={'location': '34'}, headers=make_token_header(access_token_1))
            assert resp.status_code == 400
            resp = client.patch(uri_1, data={'location': 'nairobi'}, headers=make_token_header(access_token_1))
            assert resp.status_code == 400
            # Check for input ranges
            resp = client.patch(uri_1, data={'location': '94,45'}, headers=make_token_header(access_token_1))
            assert resp.status_code == 400
            resp = client.patch(uri_1, data={'location': '34, 182'},headers=make_token_header(access_token_1))
            assert resp.status_code == 400
            resp = client.patch(uri_1, data={'location': '-94,45'}, headers=make_token_header(access_token_1))
            assert resp.status_code == 400
            resp = client.patch(uri_1, data={'location': '34, -182'}, headers=make_token_header(access_token_1))
            assert resp.status_code == 400
            resp = client.patch(uri_1, data={'location': ''}, headers=make_token_header(access_token_1))
            assert resp.status_code == 400
        if field == 'comment':
            # check that input data shoud only contain comment
            resp = client.patch(uri_1, data={'location': 'corrupt lawyers'}, headers=make_token_header(access_token_1))
            assert resp.status_code == 400
            resp = client.patch(uri_1, data={'comment': '     '}, headers=make_token_header(access_token_1))
            assert resp.status_code == 400

        # Unauthorized access
        resp = client.patch(uri_1, data=update)
        assert resp.status_code == 401
        # only access token can update
        resp = client.patch(uri_1, data=update, headers=make_token_header(refresh_token_1))
        assert resp.status_code == 422
        #
        # Check that a user can only update the record he/she created
        resp = client.patch(uri_1, data=update, headers=make_token_header(access_token_2))
        assert resp.status_code  == 403

    update_field('location')
    update_field('comment')

def test_patch_status(client):
    # Obtain tokens
    resp = client.post('/api/v2/auth/signup', data=valid_admin_data)
    assert resp.status_code == 201
    data = json.loads(resp.data.decode('utf-8'))
    data_dict = data['data'][0]
    access_token_admin = data_dict['access_token']
    refresh_token_admin = data_dict['refresh_token']
    #
    resp = client.post('/api/v2/auth/signup', data=valid_signup_data_2)
    assert resp.status_code == 201
    data = json.loads(resp.data.decode('utf-8'))
    data_dict = data['data'][0]
    access_token_2 = data_dict['access_token']

    #
    # data
    valid_update_1 = {'status': 'resolved'}
    valid_update_2 = {'status': 'unresolved'}
    valid_update_3 = {'status': 'under investigation'}
    invalid_update_1 = {'status': ''}
    invalid_update_2 = {'status': 'too little too late'}
    # create the incident to use for testing updates
    resp = client.post('/api/v2/interventions', data=user_input, headers=make_token_header(access_token_admin))
    assert resp.status_code == 201
    data = json.loads(resp.data.decode('utf-8'))
    update_uri = data['uri'] + '/' + 'status'
    print(update_uri)
    #
    resp = client.patch(update_uri, data=valid_update_1, headers=make_token_header(access_token_admin))
    assert resp.status_code == 200
    resp = client.patch(update_uri, data=valid_update_2, headers=make_token_header(access_token_admin))
    assert resp.status_code == 200
    resp = client.patch(update_uri, data=valid_update_3, headers=make_token_header(access_token_admin))
    assert resp.status_code == 200
    resp = client.patch(update_uri, data=invalid_update_1, headers=make_token_header(access_token_admin))
    assert resp.status_code == 400
    resp = client.patch(update_uri, data=invalid_update_2, headers=make_token_header(access_token_admin))
    assert resp.status_code == 400
    # Only admin can update status
    resp = client.patch(update_uri, data=valid_update_1, headers=make_token_header(access_token_2))
    assert resp.status_code == 403

def test_get_user_incidences(client):
    """
    Tests endpoint for getting all incidences
    """
    # No authorization header: should return an unauthorized error
    resp = client.get('/api/v2/users/1/interventions')
    assert resp.status_code == 401
    # get tokens
    resp = client.post('/api/v2/auth/signup', data=valid_signup_data_1)
    assert resp.status_code == 201
    data = json.loads(resp.data.decode('utf-8'))
    data_dict = data['data'][0]
    access_token = data_dict['access_token']
    refresh_token = data_dict['refresh_token']
    # Initial Request: No data
    user_id = User.get_last_inserted_id()
    uri = '/api/v2/users/{}/interventions'.format(user_id)
    resp = client.get(uri, headers=make_token_header(access_token))
    assert resp.status_code == 200
    data = json.loads(resp.data.decode('utf-8'))
    assert len(data['data']) == 0
    # add interventions
    resp = client.post('/api/v2/interventions', data=user_input, headers=make_token_header(access_token))
    assert resp.status_code == 201
    resp = client.post('/api/v2/interventions', data=user_input, headers=make_token_header(access_token))
    assert resp.status_code == 201
    # Get user unterventions
    resp = client.get(uri, headers=make_token_header(access_token))
    assert resp.status_code == 200
    data = json.loads(resp.data.decode('utf-8'))
    assert len(data['data']) == 2
