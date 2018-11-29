"""
    app.api.v1
    ~~~~~~~~~~~

    Version 1 of the RESTful API

    Creates a Blueprint instance and imports all necessary modules

"""

from flask import Blueprint

bp = Blueprint('v1', __name__)

from app.api.v1 import views, models, errors
