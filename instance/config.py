"""
    config
    ~~~~~~

    Creates an object with configuration variables

"""


import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret'
    HOSTNAME = 'localhost'
    USERNAME = 'kingkong'
    DATABASE = 'ireporterdb'

class TestConfig(Config):
    TESTING = True
    DEBUG = True

class TestDBConfig(Config):
	USERNAME = 'testuser'
	DATABASE = 'testdb'
