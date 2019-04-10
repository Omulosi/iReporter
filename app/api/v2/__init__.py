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

from app.api.v2 import incidents

#: Authentication resources
from app.api.v2.auth import SignUp, Login, RefreshToken, LogoutRefresh, LogoutAccess

#: Incident resources

#: Authentication routes
api_bp.add_resource(SignUp, '/auth/signup', endpoint='signup')
api_bp.add_resource(Login, '/auth/login', endpoint='login')
api_bp.add_resource(RefreshToken, '/auth/refresh', endpoint='refresh')
api_bp.add_resource(LogoutAccess, '/auth/logout', endpoint='logout_access')
api_bp.add_resource(LogoutRefresh, '/auth/refresh/logout', endpoint='logout_refresh')