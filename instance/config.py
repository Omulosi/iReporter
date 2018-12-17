"""
    config
    ~~~~~~

    Creates an object with configuration variables

"""
import os
from datetime import timedelta

from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:

    DBNAME = os.environ.get('DBNAME')
    USERNAME = os.environ.get('USERNAME')
    HOST = os.environ.get('HOST')
    PASSWORD = os.environ.get('PASSWORD')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
    PROPAGATE_EXCEPTIONS = True
    # MAIL_SERVER=localhost
    # MAIL_PORT=25
    MAIL_SERVER='smtp.googlemail.com'
    MAIL_PORT=587
    MAIL_USE_TLS=1
    MAIL_USERNAME='mulongojohnpaul@gmail.com'
    MAIL_PASSWORD='kleptomaniacs.9000'

class TestConfig(Config):
    TESTING = True
    DEBUG = True
    DBNAME  = 'testdb'
