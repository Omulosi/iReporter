"""
    app.api.v2
    ~~~~~~~~~~~

    Version 2 of the RESTful API

"""

from flask import Blueprint
from flask_restful import Api

bp = Blueprint('v2', __name__)
api_bp = Api(bp)

from app.api.v2 import incidents, auth

#: Authentication resources
from app.api.v2.auth import SignUp, Login, RefreshToken, LogoutRefresh, LogoutAccess

#: Incident records resources
from app.api.v2.incidents import Incidents, UpdateIncident, ReturnUserIncidents

#: Authentication routes
api_bp.add_resource(SignUp, '/auth/signup', endpoint='signup')
api_bp.add_resource(Login, '/auth/login', endpoint='login')
api_bp.add_resource(RefreshToken, '/auth/refresh', endpoint='refresh')
api_bp.add_resource(LogoutAccess, '/auth/logout', endpoint='logout_access')
api_bp.add_resource(LogoutRefresh, '/auth/refresh/logout', endpoint='logout_refresh')

#: Incident resources
api_bp.add_resource(
    Incidents,
    '/<incident_type>',
    '/<incident_type>/<_id>',
    endpoint='incidents'
    )

api_bp.add_resource(
	UpdateIncident, 
	'/<incident_type>/<_id>/<field>',
    endpoint='update_incident')

api_bp.add_resource(ReturnUserIncidents,
	'/users/<user_id>/<incident_type>',
    endpoint='user_incidents')