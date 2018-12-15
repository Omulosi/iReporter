"""
    app.api.v1
    ~~~~~~~~~~~

    Version 1 of the RESTful API

    Creates a Blueprint instance and imports all necessary modules

"""

from flask import Blueprint
from flask_restful import Api

bp = Blueprint('v1', __name__)
api_bp = Api(bp)

from app.api.v1 import views, models
