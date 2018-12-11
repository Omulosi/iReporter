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

    DBNAME = os.environ.get('DBNAME') or 'ireporterdb'
    USERNAME = os.environ.get('USERNAME') or 'jp'
    HOST = os.environ.get('HOST') or 'localhost'
    PASSWORD = os.environ.get('PASSWORD') or 'cavier'
    SECRET_KEY = os.environ.get('SECRET_KEY')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(minutes=2)

class TestConfig(Config):
    TESTING = True
    DEBUG = True
    DBNAME  = 'testdb'
