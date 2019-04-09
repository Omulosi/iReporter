"""
    app.tests.v1.views
    ~~~~~~~~~~~~~~~~~~~

    Tests for the API endpoints

"""
from app import create_app
from instance.config import TestConfig
from app.api.v1.models import Record as db
from datetime import datetime
import pytest
import json

@pytest.fixture
def client():
    """
    Configures the application for testing.
    This fixture is called for each individual test.
    """
    app = create_app(TestConfig)
    client = app.test_client()

    # Create an application context before running the tests
    ctx = app.app_context()
    ctx.push()

    yield client

    db.clear_all()
    ctx.pop()

user_input = {'location': '-1.23, 36.5', 'comment':'crooked tendering processes'}

def test_get_all(client):
    """
    Tests endpoint for getting all requests
    """
    # Initially no data present. Request should still be successful
    resp = client.get('/api/v1/red-flags')
    assert resp.status_code == 200
    data = json.loads(resp.data.decode('utf-8'))
    assert len(data['data']) == 0
    resp = client.post('/api/v1/red-flags', data=user_input)
    resp = client.get('/api/v1/red-flags')
    assert resp.status_code == 200
    assert b'data'in resp.data
    assert b'status' in resp.data
    data = json.loads(resp.data.decode('utf-8'))
    assert len(data['data']) == 1
    data = json.loads(resp.data.decode('utf-8'))
    data = data['data'][0] # Returns a dictionary of data item
    assert data.get('location') == '-1.23, 36.5'
    assert data.get('comment') # comment field must be present
    assert type(data.get('type')) == str
    assert type(data.get('status')) == str
    assert type(data.get('createdBy')) == int
    assert type(data.get('id')) == int
    assert type(data.get('Images')) == list
    assert type(data.get('Videos')) == list

def test_post(client):
    """
    Tests the create red-flag endpoint
    """
    resp = client.post('/api/v1/red-flags', data=user_input)
    assert resp.status_code == 201
    assert b'data' in resp.data
    assert b'status' in resp.data
    # Check that returned data has all fields and contains user input data
    data = json.loads(resp.data.decode('utf-8'))
    data = data['data'][0] # Returns a dictionary of data item
    assert data.get('location') == '-1.23, 36.5'
    assert data.get('comment') # comment field must be present
    assert type(data.get('type')) == str
    assert type(data.get('status')) == str
    assert type(data.get('createdBy')) == int
    assert type(data.get('id')) == int
    assert type(data.get('Images')) == list
    assert type(data.get('Videos')) == list
    assert resp.mimetype == 'application/json'
    assert resp.headers['Location'] is not None
    # Missing field(s) in request
    resp = client.post('/api/v1/red-flags', data={'location': '23,53'})
    assert resp.status_code ==  400
    resp = client.post('/api/v1/red-flags', data={'comment': 'thief'})
    assert resp.status_code ==  400
    resp = client.post('/api/v1/red-flags', data=None)
    assert resp.status_code ==  400
    # input data should not be blank
    resp = client.post('/api/v1/red-flags', data={'location': '', 'comment':''})
    assert resp.status_code ==  400
    # Too many input fields
    resp = client.post('/api/v1/red-flags', data={'location': '20,20', 'comment':'corruption', '_type':'red-flag'})
    assert resp.status_code ==  400
    # Check latitude ranges
    resp = client.post('/api/v1/red-flags', data={'location': '93,23'})
    assert resp.status_code ==  400
    resp = client.post('/api/v1/red-flags', data={'location': '-91,23'})
    assert resp.status_code ==  400
    # Check longitude ranges
    resp = client.post('/api/v1/red-flags', data={'location': '34,181'})
    assert resp.status_code ==  400
    resp = client.post('/api/v1/red-flags', data={'location': '45,-183'})
    assert resp.status_code ==  400

def test_get_one(client):
    resp = client.post('/api/v1/red-flags', data=user_input)
    assert resp.status_code == 201
    start = resp.headers['Location'].find('api')
    uri = '/' + resp.headers['Location'][start:]
    resp = client.get(uri)
    assert resp.status_code == 200
    assert resp.headers['Content-Type'] == 'application/json'
    assert b'data' in resp.data
    assert b'status' in resp.data
    # Check that returned data has all fields and contains user input data
    data = json.loads(resp.data.decode('utf-8'))
    data = data['data'][0] # Returns a dictionary of data item
    assert data.get('location') == '-1.23, 36.5'
    assert data.get('comment') # comment field must be present
    assert type(data.get('type')) == str
    assert type(data.get('status')) == str
    assert type(data.get('createdBy')) == int
    assert type(data.get('id')) == int
    assert type(data.get('Images')) == list
    assert type(data.get('Videos')) == list
    # Item not found - ID out of range
    resp = client.get('/api/v1/red-flags/999')
    assert resp.status_code == 404
    assert resp.headers['Content-Type'] == 'application/json'
    # Invalid ID
    resp = client.get('/api/v1/red-flags/some-id')
    assert resp.status_code == 404
    assert resp.headers['Content-Type'] == 'application/json'

def test_delete_one(client):
    # create a red-flag to use for testing deletion
    resp = client.post('/api/v1/red-flags', data=user_input)
    assert resp.status_code == 201
    start = resp.headers['Location'].find('api')
    uri = '/' + resp.headers['Location'][start:]
    #
    resp = client.delete(uri)
    assert resp.status_code  == 200
    assert b'data' in resp.data
    assert b'status' in  resp.data
    # check that deletion is successful
    resp = client.get(uri)
    assert resp.status_code == 404
    assert resp.headers['Content-Type'] == 'application/json'
    # Item not present
    resp = client.delete('/api/v1/red-flags/9999')
    assert resp.status_code == 404
    assert resp.headers['Content-Type'] ==  'application/json'
    # Invalid ID
    resp = client.delete('/api/v1/red-flags/data-id')
    assert resp.status_code == 404
    assert resp.headers['Content-Type'] == 'application/json'

def test_patch_location_or_comment(client):
    def update_field(field):
        # create the redflag to use for testing updates
        resp = client.post('/api/v1/red-flags', data=user_input)
        assert resp.status_code == 201
        start = resp.headers['Location'].find('api')
        uri = '/' + resp.headers['Location'][start:]
        update_uri = uri + '/' + field
        # check update of location field is successful(valid input)
        if field == 'location':
            update = {'location': '-15.7, 77.2'}
        if field == 'comment':
            update = {'comment': 'new updated comment'}
        resp = client.patch(update_uri, data=update)
        assert resp.status_code  == 200
        assert b'data' in resp.data
        assert b'status' in  resp.data
        data = json.loads(resp.data.decode('utf-8'))
        assert data['data'][0]['message'] == field + ' has been successfully updated'
        assert data['data'][0]['record']
        # Item not present - ID out of range
        resp = client.patch('/api/v1/red-flags/10000/' + field)
        assert resp.status_code == 404
        assert resp.headers['Content-Type'] ==  'application/json'
        # Invalid ID
        resp = client.patch('/api/v1/red-flags/that-record/' + field)
        assert resp.status_code == 404
        assert resp.headers['Content-Type'] == 'application/json'
        #
        # Too many input fields
        resp = client.patch(update_uri, data={'location': '34,34', 'comment': 'corrupt lawyers'})
        assert resp.status_code == 400
        if field == 'location':
            # only location should be in input data
            resp = client.patch(update_uri, data={'comment': 'corrupt lawyers'})
            assert resp.status_code == 400
            # check for invalid location format
            resp = client.patch(update_uri, data={'location': '34'})
            assert resp.status_code == 400
            resp = client.patch(update_uri, data={'location': 'nairobi'})
            assert resp.status_code == 400
            # Check for input ranges
            resp = client.patch(update_uri, data={'location': '94,45'})
            assert resp.status_code == 400
            resp = client.patch(update_uri, data={'location': '34, 182'})
            assert resp.status_code == 400
            resp = client.patch(update_uri, data={'location': '-94,45'})
            assert resp.status_code == 400
            resp = client.patch(update_uri, data={'location': '34, -182'})
            assert resp.status_code == 400
        if field == 'comment':
            # check that input data shoud only contain comment
            resp = client.patch(update_uri, data={'location': 'corrupt lawyers'})
            assert resp.status_code == 400

    update_field('location')
    update_field('comment')
