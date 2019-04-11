"""
    tests.v1.conftest
    ~~~~~~~~~~~~~~

    This module contains functions for configuring the application
    for testing
"""

from app import create_app
from config import TestConfig
from app.api.v1.models import Record as db
import pytest

@pytest.fixture
def app():

    app = create_app(TestConfig)
   
    with app.app_context():
       
        yield app

    db.clear_all()


@pytest.fixture
def client(app):
    return app.test_client()