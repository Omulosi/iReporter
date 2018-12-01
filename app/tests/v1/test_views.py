"""
    app.tests.v1.views
    ~~~~~~~~~~~~~~~~~~~

    Tests for the API endpoints

"""
from app import create_app
from instance.config import TestConfig
from app.api.v1.models import Record as db
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

def test_post(client):
    """
    Tests the create red-flag endpoint
    """
    resp = client.post('/api/v1/red-flags', data=user_input)
    assert resp.status_code == 201
    assert b'data' in resp.data
    assert b'status' in resp.data
    data = json.loads(resp.data.decode('utf-8'))
    assert 'red-flag record' in data['data'][0]['message']
    assert resp.mimetype == 'application/json'
    assert resp.headers['Location'] is not None
    # Missing fields in request
    resp = client.post('/api/v1/red-flags', data={'location': '23,23'})
    assert resp.status_code ==  400
    resp = client.post('/api/v1/red-flags', data={'comment': 'thief'})
    assert resp.status_code ==  400
    resp = client.post('/api/v1/red-flags', data=None)
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
    # Item not found
    resp = client.get('/api/v1/red-flags/999')
    assert resp.status_code == 404
    assert resp.headers['Content-Type'] == 'application/json'
    # Invalid ID
    resp = client.get('/api/v1/red-flags/data-id')
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

def test_patch_location_and_comment(client):
    def update_field(field):
        resp = client.post('/api/v1/red-flags', data=user_input)
        assert resp.status_code == 201
        start = resp.headers['Location'].find('api')
        uri = '/' + resp.headers['Location'][start:]
        update_uri = uri + '/' + field
        # check update of location field is successful
        if field == 'location':
            update = {'location': '-15.7, 77.2'}
        if field == 'comment':
            update = {'comment': 'new updated comment'}
        resp = client.patch(update_uri, data=update)
        assert resp.status_code  == 200
        assert b'data' in resp.data
        assert b'status' in  resp.data
        data = json.loads(resp.data.decode('utf-8'))
        assert 'Updated' in data['data'][0]['message']
        # Item not present
        resp = client.patch('/api/v1/red-flags/10000/' + field)
        assert resp.status_code == 404
        assert resp.headers['Content-Type'] ==  'application/json'
        # Invalid ID
        resp = client.patch('/api/v1/red-flags/that-record/' + field)
        assert resp.status_code == 404
        assert resp.headers['Content-Type'] == 'application/json'

    update_field('location')
    update_field('comment')

