"""
    config
    ~~~~~~

    Creates an object with configuration variables

"""

import os

class Config:
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret'
	HOSTNAME = 'localhost'
	USERNAME = 'omulosi'

class TestConfig(Config):
    TESTING = True
    DEBUG = True
    DATABASE = 'test_db'

class DatabaseConfig(Config):

	DATABASE = 'ireporter_db'

