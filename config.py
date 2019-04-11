
'''
    instance.config
    ------------------
    This module provides default configuration values.
'''

import os
from datetime import timedelta

from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    '''
    Base configuration values
    '''

    SECRET_KEY = os.environ.get('SECRET_KEY')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
    PROPAGATE_EXCEPTIONS = True
    
    #: Database url
    DATABASE = os.getenv('DB_URL')

    #: Mail server configuration values
    MAIL_SERVER=os.environ.get('MAIL_SERVER')
    MAIL_PORT=os.environ.get('MAIL_PORT')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_USE_TLS=os.environ.get('MAIL_USE_TLS')
    MAIL_USERNAME=os.environ.get('MAIL_USERNAME')

    #: settigs for sending mail using sendgrid
    SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')

    ADMIN_EMAIL = 'no-reply@ireporter.com'

class TestConfig(Config):
    '''
    configuration values for testing
    '''
    
    TESTING = True
    DEBUG = True
    PROPAGATE_EXCEPTIONS = True
    DATABASE = os.environ.get('TEST_DB_URL')

