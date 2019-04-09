"""
    app.tests.v2.incidents
    ~~~~~~~~~~~~~~~~~~~~~~
"""
import json
from app.helpers import make_token_header
from app.api.v2.models import User


#: test data
DATA = {'location': '-1.23, 36.5', 'comment':'crooked tendering processes'}

def test_get_all_incidences(client, auth):
    """
    Tests endpoint for getting all incidences
    """
    #:  No authorization header: should return an unauthorized error
    resp = client.get('/api/v2/interventions')
    assert resp.status_code == 401

    #: Sign in and acquire tokens
    resp = auth.login()
    data = json.loads(resp.data.decode('utf-8'))['data'][0]
    access_token, refresh_token = data['access_token'], data['refresh_token']

    # Initial Request: No data
    resp = client.get('/api/v2/interventions', headers=make_token_header(access_token))
    assert resp.status_code == 200
    data = json.loads(resp.data.decode('utf-8'))
    assert not data['data']

    #: Add test data
    resp = client.post('/api/v2/interventions', data=DATA, headers=make_token_header(access_token))
    assert resp.status_code == 201

    # Return test data
    resp = client.get('/api/v2/interventions', headers=make_token_header(access_token))
    assert resp.status_code == 200
    assert b'data'in resp.data
    assert b'status' in resp.data
    data = json.loads(resp.data.decode('utf-8'))
    assert data['data']

def test_create_incident(client, auth):
    """
    Tests the create incident endpoint
    """

    #: Unauthorized - no token
    resp = client.post('/api/v2/interventions', data=DATA)
    assert resp.status_code == 401

    #: Sign in and acquire tokens
    resp = auth.login()
    data = json.loads(resp.data.decode('utf-8'))['data'][0]
    access_token, refresh_token = data['access_token'], data['refresh_token']

    # create record
    resp = client.post('/api/v2/interventions', data=DATA, headers=make_token_header(access_token))
    assert resp.status_code == 201
    data = json.loads(resp.data.decode('utf-8'))
    data = data['data'][0]
    assert resp.mimetype == 'application/json'
    assert resp.headers['Location'] is not None

def test_create_incident_validate(client, auth):
    """
    Tests for checking data validity for endpoint for creating an incident
    """

    #: Sign in and acquire tokens
    resp = auth.login()
    data = json.loads(resp.data.decode('utf-8'))['data'][0]
    access_token, refresh_token = data['access_token'], data['refresh_token']

    #: Only access tokens allowed
    resp = client.post('/api/v2/interventions', data=DATA, headers=make_token_header(refresh_token))
    assert resp.status_code == 422

    #: Missing required fields 
    resp = client.post('/api/v2/interventions', data={'location': '23,53'}, headers=make_token_header(access_token))
    assert resp.status_code ==  400
    resp = client.post('/api/v2/interventions', data={'comment': 'thief'}, headers=make_token_header(access_token))
    assert resp.status_code ==  400
    resp = client.post('/api/v2/interventions', data=None, headers=make_token_header(access_token))
    assert resp.status_code ==  400

    #: Input fields with white-space
    resp = client.post('/api/v2/interventions', data={'location': '', 'comment':''}, headers=make_token_header(access_token))
    assert resp.status_code ==  400
    resp = client.post('/api/v2/interventions', data={'location': '     ', 'comment':'      '}, headers=make_token_header(access_token))
    assert resp.status_code ==  400

    #: Invalid data for location fields
    resp = client.post('/api/v2/interventions', data={'location': '93,23'}, headers=make_token_header(access_token))
    assert resp.status_code ==  400
    resp = client.post('/api/v2/interventions', data={'location': '-91,23'}, headers=make_token_header(access_token))
    assert resp.status_code ==  400
    resp = client.post('/api/v2/interventions', data={'location': '34,181'}, headers=make_token_header(access_token))
    assert resp.status_code ==  400
    resp = client.post('/api/v2/interventions', data={'location': '45,-183'}, headers=make_token_header(access_token))
    assert resp.status_code ==  400

def test_get_incident(client, auth):
    """
    Tests for endpoint that returns a single record
    """
    #: Sign in and acquire tokens
    resp = auth.login()
    data = json.loads(resp.data.decode('utf-8'))['data'][0]
    access_token, refresh_token = data['access_token'], data['refresh_token']

    #: Create test data
    resp = client.post('/api/v2/interventions', data=DATA, headers=make_token_header(access_token))
    assert resp.status_code == 201
    data = json.loads(resp.data.decode('utf-8'))
    uri = data['uri']

    #: Get the test data
    resp = client.get(uri, headers=make_token_header(access_token))
    assert resp.status_code == 200
    data = json.loads(resp.data.decode('utf-8'))
    #: check all fields are present
    data = data['data']
    assert data['location']
    assert data['comment']
    assert ['type']
    assert ['status']
    assert ['createdBy']
    assert ['id']
    assert ['Images']
    assert ['Videos']

def test_get_incident_validate(client, auth):
    """
    Tests for request validity for endpoint that returns a single record
    """

    #: Sign in and acquire tokens
    resp = auth.login()
    data = json.loads(resp.data.decode('utf-8'))['data'][0]
    access_token, refresh_token = data['access_token'], data['refresh_token']

    #: Invalid requests - bad ID
    resp = client.get('/api/v1/interventions/999', headers=make_token_header(access_token))
    assert resp.status_code == 404
    resp = client.get('/api/v2/interventions/some-id', headers=make_token_header(access_token))
    assert resp.status_code == 404

    #: Missing authorizartion header
    resp = client.post('/api/v2/interventions', data=DATA)
    assert resp.status_code == 401

def test_delete_incident(client, auth):
    """
    Tests for the delete incident endpoint
    """
    #: Sign in and acquire tokens
    resp = auth.login()
    data = json.loads(resp.data.decode('utf-8'))['data'][0]
    access_token, refresh_token = data['access_token'], data['refresh_token']

    #: create test data
    resp = client.post('/api/v2/interventions', data=DATA, headers=make_token_header(access_token))
    data = json.loads(resp.data.decode('utf-8'))
    uri = data['uri']

    # Delete test data
    resp = client.delete(uri, headers=make_token_header(access_token))
    assert resp.status_code  == 200
    assert b'data' in resp.data
    assert b'status' in  resp.data

    #: Test data should no longer exist
    resp = client.get(uri, headers=make_token_header(access_token))
    assert resp.status_code == 404

def test_delete_incident_validate(client, auth):
    """
    Tests for checking validity of requests for delete endpoint
    """

    #: Sign in and acquire tokens
    resp = auth.login()
    data = json.loads(resp.data.decode('utf-8'))['data'][0]
    access_token_1, refresh_token_1 = data['access_token'], data['refresh_token']

    #: Accessing delete endpoint with no authorization header
    resp = client.delete('/api/v2/interventions/1')
    assert resp.status_code == 401

    #: Using invalid IDs
    resp = client.delete('/api/v2/interventions/9999', headers=make_token_header(access_token_1))
    assert resp.status_code == 404
    resp = client.delete('/api/v2/interventions/data-id', headers=make_token_header(access_token_1))
    assert resp.status_code == 404

    #: Refresh tokens cannot access delete endpoint
    resp = client.delete('/api/v2/interventions/9999', headers=make_token_header(refresh_token_1))
    assert resp.status_code == 422
    

    #: A user can only delete own record
    #: Create second user and obtain associated tokens
    resp = auth.signup(username='patrice', password='lumumba')
    data = json.loads(resp.data.decode('utf-8'))['data'][0]
    access_token_2 = data['access_token']
    
    #: create test data for user-1
    resp = client.post('/api/v2/interventions', data=DATA,
            headers=make_token_header(access_token_1))
    data = json.loads(resp.data.decode('utf-8'))
    uri_1 = data['uri']
    #: create test-data for user-2
    resp = client.post('/api/v2/interventions', data=DATA, headers=make_token_header(access_token_2))
    data = json.loads(resp.data.decode('utf-8'))
    uri_2 = data['uri']
    
    #: user-1 cannot delete user-2's data
    resp = client.delete(uri_2, headers=make_token_header(access_token_1))
    assert resp.status_code == 403
    #: user-2 cannot delete user-1's data
    resp = client.delete(uri_1, headers=make_token_header(access_token_2))
    assert resp.status_code == 403

def test_patch_location(client, auth):

    field = 'location'
    #: Sign in and acquire tokens
    resp = auth.login()
    data = json.loads(resp.data.decode('utf-8'))['data'][0]
    access_token_1, refresh_token_1 = data['access_token'], data['refresh_token']

    #: create test data 
    resp = client.post('/api/v2/interventions', 
                        data={'location': '-1.23, 36.5', 'comment':'crooked tendering processes'}, 
                        headers=make_token_header(access_token_1))
    data = json.loads(resp.data.decode('utf-8'))
    uri_1 = data['uri'] + '/' + field

    #: update location field
    resp = client.patch(uri_1, data={'location': '-15.7, 77.2'}, headers=make_token_header(access_token_1))
    assert resp.status_code  == 200
    assert b'data' in resp.data
    assert b'status' in  resp.data

def test_patch_comment(client, auth):

    field = 'comment'

    #: Sign in and acquire tokens
    resp = auth.login()
    data = json.loads(resp.data.decode('utf-8'))['data'][0]
    access_token, refresh_token = data['access_token'], data['refresh_token']

    #: create test data
    resp = client.post('/api/v2/interventions',
                       data={'location': '-1.23, 36.5', 'comment':'crooked tendering processes'},
                       headers=make_token_header(access_token))
    data = json.loads(resp.data.decode('utf-8'))
    uri_1 = data['uri'] + '/' + field

    #: update comment field
    resp = client.patch(uri_1, data={'comment': 'lipa kama tender'},
                        headers=make_token_header(access_token))
    assert resp.status_code == 200
    assert b'data' in resp.data
    assert b'status' in  resp.data

def test_patch_location_validate(client, auth):
    """
    Tests for validity of requests to patch location endpoint
    """
    field = 'location'

    #: Sign in and acquire tokens for user-1
    resp = auth.login()
    data = json.loads(resp.data.decode('utf-8'))['data'][0]
    access_token_1, refresh_token_1 = data['access_token'], data['refresh_token']

    #: acquire tokens for user-2
    resp = auth.signup(username='patrice', password='lumumba')
    data = json.loads(resp.data.decode('utf-8'))['data'][0]
    access_token_2 = data['access_token']
    refresh_token_2= data['refresh_token']

    #: create test data for user-1
    resp = client.post('/api/v2/interventions', 
                        data={'location': '-1.23, 36.5', 'comment':'crooked tendering processes'}, 
                        headers=make_token_header(access_token_1))
    data = json.loads(resp.data.decode('utf-8'))
    uri_1 = data['uri'] + '/' + field
    
    #: Invalid IDs
    resp = client.patch('/api/v2/interventions/10000/' + field, headers=make_token_header(access_token_1))
    assert resp.status_code == 404
    resp = client.patch('/api/v2/interventions/record/' + field, headers=make_token_header(access_token_1))
    assert resp.status_code == 404
    
    #: Too many input fields
    resp = client.patch(uri_1, data={'location': '34,34', 'comment': 'corrupt lawyers'}, headers=make_token_header(access_token_1))
    assert resp.status_code == 400
    
    #: Only location should be in input data
    resp = client.patch(uri_1, data={'comment': 'corrupt lawyers'}, headers=make_token_header(access_token_1))
    assert resp.status_code == 400

    #: Invalid data for location
    resp = client.patch(uri_1, data={'location': '34'}, headers=make_token_header(access_token_1))
    assert resp.status_code == 400
    resp = client.patch(uri_1, data={'location': 'nairobi'}, headers=make_token_header(access_token_1))
    assert resp.status_code == 400

    #: Input data exceeeds valid limits
    resp = client.patch(uri_1, data={'location': '94,45'}, headers=make_token_header(access_token_1))
    assert resp.status_code == 400
    resp = client.patch(uri_1, data={'location': '34, 182'},headers=make_token_header(access_token_1))
    assert resp.status_code == 400
    resp = client.patch(uri_1, data={'location': '-94,45'}, headers=make_token_header(access_token_1))
    assert resp.status_code == 400
    resp = client.patch(uri_1, data={'location': '34, -182'}, headers=make_token_header(access_token_1))
    assert resp.status_code == 400

    #: Empty location field
    resp = client.patch(uri_1, data={'location': ''}, headers=make_token_header(access_token_1))
    assert resp.status_code == 400

    #: No access header
    resp = client.patch(uri_1, data={'location': '20,29'})
    assert resp.status_code == 401

    #: Only access token can update a field
    resp = client.patch(uri_1, data={'location': '30,30'}, headers=make_token_header(refresh_token_1))
    assert resp.status_code == 422
    
    #: A user can only update own record
    resp = client.patch(uri_1, data={'location':'30,30'}, headers=make_token_header(access_token_2))
    assert resp.status_code  == 403

def test_patch_comment_validate(client, auth):
    """
    Tests for validity of requests to patch comment endpoint
    """

    field = 'comment'
    update = {'comment': 'new comment'}

    #: Sign in and acquire tokens for user-1
    resp = auth.login()
    data = json.loads(resp.data.decode('utf-8'))['data'][0]
    access_token_1, refresh_token_1 = data['access_token'], data['refresh_token']

    #: acquire tokens for user-2
    resp = auth.signup(username='patrice', password='lumumba')
    data = json.loads(resp.data.decode('utf-8'))['data'][0]
    access_token_2 = data['access_token']
    refresh_token_2= data['refresh_token']

    #: create test data for user-1
    resp = client.post('/api/v2/interventions', 
                        data={'location': '-1.23, 36.5', 'comment':'crooked tendering processes'}, 
                        headers=make_token_header(access_token_1))
    data = json.loads(resp.data.decode('utf-8'))
    uri_1 = data['uri'] + '/' + field
    
    
    #: Invalid IDs
    resp = client.patch('/api/v2/interventions/10000/comment', headers=make_token_header(access_token_1))
    assert resp.status_code == 404
    resp = client.patch('/api/v2/interventions/record/comment', headers=make_token_header(access_token_1))
    assert resp.status_code == 404
    
    #: Too many input fields
    resp = client.patch(uri_1, data={'location': '34,34', 'comment': 'corrupt lawyers'}, headers=make_token_header(access_token_1))
    assert resp.status_code == 400
    
    #: Only comment should be in input data
    resp = client.patch(uri_1, data={'location': '34,55'}, headers=make_token_header(access_token_1))
    assert resp.status_code == 400


    #: Invalid comment data
    resp = client.patch(uri_1, data={'comment': '  '}, headers=make_token_header(access_token_1))
    assert resp.status_code == 400
    resp = client.patch(uri_1, data={'comment': ''}, headers=make_token_header(access_token_1))
    assert resp.status_code == 400

    #: No access header
    resp = client.patch(uri_1, data=update)
    assert resp.status_code == 401

    #: Only access token can update a field
    resp = client.patch(uri_1, data=update, headers=make_token_header(refresh_token_1))
    assert resp.status_code == 422
    
    #: A user can only update own record
    resp = client.patch(uri_1, data=update, headers=make_token_header(access_token_2))
    assert resp.status_code  == 403

def test_patch_status(client, auth):
    """ tests for updating status field of a record
    """

    #: create admin user
    resp = auth.signup(username='patrice', password='lumumba', admin=True)
    data = json.loads(resp.data.decode('utf-8'))['data'][0]
    access_token_admin = data['access_token']
    refresh_token_admin = data['refresh_token']
    
    #: Sign in and acquire tokens for normal user
    resp = auth.login()
    data = json.loads(resp.data.decode('utf-8'))['data'][0]
    access_token, refresh_token = data['access_token'], data['refresh_token']

    #: use admin to create the incident to use for testing updates
    resp = client.post('/api/v2/interventions', 
                        data={'location': '-1.23, 36.5', 'comment':'crooked tendering processes'}, 
                        headers=make_token_header(access_token_admin))
    data = json.loads(resp.data.decode('utf-8'))
    update_uri = data['uri'] + '/' + 'status'

    #: test data
    invalid_update_1 = {'status': ''}
    invalid_update_2 = {'status': 'too little too late'}
    
    #: admin can update status field with the three valid inputs
    resp = client.patch(update_uri, data={'status': 'resolved'}, headers=make_token_header(access_token_admin))
    assert resp.status_code == 200
    resp = client.patch(update_uri, data={'status': 'unresolved'}, headers=make_token_header(access_token_admin))
    assert resp.status_code == 200
    resp = client.patch(update_uri, data={'status': 'under investigation'}, headers=make_token_header(access_token_admin))
    assert resp.status_code == 200

    #: Invalid data for status
    resp = client.patch(update_uri, data={'status': ''}, headers=make_token_header(access_token_admin))
    assert resp.status_code == 400
    resp = client.patch(update_uri, data={'status': '   '}, headers=make_token_header(access_token_admin))
    assert resp.status_code == 400
    resp = client.patch(update_uri, data={'status': 'too little too late'}, headers=make_token_header(access_token_admin))
    assert resp.status_code == 400

    #: Only admin can update status
    resp = client.patch(update_uri, data={'status': 'resolved'}, 
            headers=make_token_header(access_token))
    assert resp.status_code == 403

def test_get_user_incidences(client, auth):
    """
    Tests endpoint for getting all incidences
    """
    #: Sign in and acquire tokens for user-1
    resp = auth.login()
    data = json.loads(resp.data.decode('utf-8'))['data'][0]
    access_token, refresh_token = data['access_token'], data['refresh_token']

    #: No authorization header
    resp = client.get('/api/v2/users/1/interventions')
    assert resp.status_code == 401
   
    #: Initial Request- no data
    user_id = User.get_last_inserted_id()
    uri = '/api/v2/users/{}/interventions'.format(user_id)
    resp = client.get(uri, headers=make_token_header(access_token))
    assert resp.status_code == 200
    data = json.loads(resp.data.decode('utf-8'))
    assert not data['data']

    #: create a record
    resp = client.post('/api/v2/interventions', 
                        data={'location': '-1.23, 36.5', 'comment':'crooked tendering processes'}, 
                        headers=make_token_header(access_token))

    #: Get user specific records
    resp = client.get(uri, headers=make_token_header(access_token))
    assert resp.status_code == 200
    data = json.loads(resp.data.decode('utf-8'))
    assert data['data']
