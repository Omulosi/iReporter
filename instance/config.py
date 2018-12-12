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
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=60)

class TestConfig(Config):
    TESTING = True
    DEBUG = True
    DBNAME  = 'testdb'
