from flask_restful import Resource, reqparse, url_for
from . import api_bp
from .database import get_by_id, get_all, put_item, delete_item, update_item, connect, User, get_by_username
from .errors import raise_error
from .database import check_password

from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)



class UserSignup(Resource):
    """
    User sign up endpoint
    """

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username', type=str, required=True, help='username not provided')
        self.parser.add_argument('password', type=str, required=True, help='password not provided')
        self.parser.add_argument('email', type=str, required=True, help='email not provided')
        super(UserSignup, self).__init__()

	def post(self):
		data = self.parser.parse_args() 
		username = data.get('username')
		password = data.get('password')
		email = data.get('email')
		username_exists = get_by_username(username)
		if username_exists:
			return raise_error(400, "Use a different username")
		email_exists = get_by_email(email)
		if email_exists:
			return raise_error(400, "Use a different email")
		user = User(username=username, email=email)
		user.set_password(password)
		put_item(user)
		token = create_access_token(identity = data['username'])
		output = {}
		output['status'] = 200
		output['data'] = [{'token': token, 'user': user.serialize }]
		return output

class UserLogin(Resource):
	"""
	User login endpoint
	"""

	def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username', type=str, required=True, help='username not provided')
        self.parser.add_argument('password', type=str, required=True, help='password not provided')
        super(UserLogin, self).__init__()

	def post(self):
		data = self.parser.parse_args() 
		username = data.get('username')
		password = data.get('password')
		current_user = get_by_username(username)
		if not current_user:
			return raise_error(400, 'User does not exist')
		user = current_user[0]
		pass_hash = current_user['password_hash']
		if check_password(pass_hash, password):
			token = create_access_token(identity = username)
			output = {}
			output['status'] = 200
			output['data'] = [{'token': token, 'user': current_user }]
			user = User(username=username)
		else:
			return raise_error(401, "Invalid credentials")






api_bp.add_resource(UserSignup, '/auth/signup', endpoint='signup')
api_bp.add_resource(UserLogin, '/auth/login', endpoint='login')
