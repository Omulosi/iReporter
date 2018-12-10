"""
    config
    ~~~~~~

    Creates an object with configuration variables

"""
import os

from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    DBNAME  = os.environ.get('DBNAME') or 'ireporterdb'
    USERNAME = os.environ.get('USERNAME') or 'jp'
    HOST = os.environ.get('HOST') or 'localhost'
    PASSWORD = os.environ.get('PASSWORD') or 'cavier'

class TestConfig(Config):
    TESTING = True
    DEBUG = True
    DBNAME  = 'testdb'
