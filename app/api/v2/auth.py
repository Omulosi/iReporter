"""
    app.api.v2.auth
    ~~~~~~~~~~~~~~~~~

    Implements API endpoints

"""
from flask_restful import Resource, reqparse, url_for
from . import api_bp
from .models import Record, User
from .errors import raise_error
from werkzeug.security import check_password_hash

class SignUp(Resource):
	"""
	Implements method for signing up a suser
	"""
	def post(self):
		return {'username': 'john'}

class Login(Resource):
	"""
	Implements login methods
	"""
	def post(self):
		return {'loggedin': 'john'}
		

#
# API resource routing
#

api_bp.add_resource(SignUp, '/auth/signup', endpoint='signup')
api_bp.add_resource(Login, '/auth/login', endpoint='login')