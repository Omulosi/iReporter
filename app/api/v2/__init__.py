"""
    app.api.v2
    ~~~~~~~~~~~

    Version 2 of the RESTful API

    Creates a Blueprint instance and imports all necessary modules

"""

from flask import Blueprint
from flask_restful import Api

bp = Blueprint('v2', __name__)
api_bp = Api(bp)

from app.api.v2 import models, auth, incidents
