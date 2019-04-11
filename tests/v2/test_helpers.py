'''
	tests.v2.test_helpers
	----------------------

	Tests for helper functions
'''
from app.helpers import make_token_header, send_email
import json

def test_make_token_header():
    token_header = make_token_header('some-token')
    assert 'Authorization' in token_header