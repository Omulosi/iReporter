"""
    config
    ~~~~~~

    Creates an object with configuration variables

"""

class Config:
   SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret'

class TestConfig(Config):
    TESTING = True
    DEBUG = True

class DatabaseConfig(Config):
    HOSTNAME = 'localhost'
    USERNAME = 'omulosi'
    DATABASE = 'ireporter'

