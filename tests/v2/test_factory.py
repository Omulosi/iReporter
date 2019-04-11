'''
	tests.v2.test_factory
	---------------------

	Tests for the application factory
'''

from app import create_app
from instance.config import TestConfig

def test_config():
    assert not create_app().testing
    assert create_app(TestConfig).testing