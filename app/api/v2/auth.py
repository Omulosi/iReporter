"""
    app.api.v2.auth
    ~~~~~~~~~~~~~~~~~

    Implements authentication and authorization functionality (Sign In and Sign Up)

"""

from flask_jwt_extended import (create_access_token, create_refresh_token, 
                                jwt_refresh_token_required, get_jwt_identity)
from flask_restful import Resource, reqparse
from app.api.errors import raise_error
from app.api.utils import valid_username, valid_email, valid_password, update_createdon
from .models import  User
from . import api_bp


class SignUp(Resource):
    """
    Implements method for signing up a user
    """
    def __init__(self):

        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username', type=str, required=True,
                                 help='Please enter username and password')
        self.parser.add_argument('password', type=str, required=True,
                                 help='Please enter username and password')
        # Optional fields
        self.parser.add_argument('email', type=str)
        self.parser.add_argument('phone', type=str)
        self.parser.add_argument('firstname', type=str)
        self.parser.add_argument('lastname', type=str)
        self.parser.add_argument('othernames', type=str)
        self.parser.add_argument('isadmin', type=str)
        super(SignUp, self).__init__()

    def post(self):
        """
        Registers a new user
        """
        data = self.parser.parse_args()
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        phone = data.get('phone')
        firstname = data.get('firstname')
        lastname = data.get('lastname')
        othernames = data.get('othernames')
        isadmin = data.get('isadmin')

        username = valid_username(username)
        if not username:
            return raise_error(400, "Invalid Username. It should be at least 3 characters long and"
                               "the first character should be a letter.")
        if User.filter_by('username', username):
            return raise_error(400, "Please use a different username")
        if email and not valid_email(email):
            return raise_error(400, "Invalid email format")
        if email and User.filter_by('email', email):
            return raise_error(400, "Please use a different email")
        if not valid_password(password):
            return raise_error(400, "Invalid password. "
                               "Ensure the password is at least 5 characters long")
        user = User(username=username, password=password, email=email, firstname=firstname,
                    lastname=lastname, othernames=othernames, phone_number=phone, isadmin=isadmin)
        user.put()
        access_token = create_access_token(identity=username, fresh=True)
        refresh_token = create_refresh_token(identity=username)

        return {
            'status': 201,
            'data': [{'access_token': access_token,
                      'refresh_token': refresh_token,
                      'user': user.serialize
                     }]
            }, 201

class Login(Resource):
    """
    Implements login endpoint. The endpoint returns an access and
    a fresh token on successful request.
    """
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username', type=str, required=True,
                                 help='Please enter username and password')
        self.parser.add_argument('password', type=str, required=True,
                                 help='Please enter username and password')
        super(Login, self).__init__()

    def post(self):
        """
        Logs in a user
        """
        data = self.parser.parse_args()
        username = data.get('username')
        password = data.get('password')
        user = User.by_username(username)
        p_hash = user.get('password_hash', '')
        if not user or not User.check_password(p_hash, password):
            return raise_error(401, "Invalid username or password")
        access_token = create_access_token(identity=username, fresh=True)
        refresh_token = create_refresh_token(identity=username)
        user = {field_name: field_val for field_name, field_val
                in user.items() if field_name != 'password_hash'}
        user = update_createdon(user)
        return {
            'status': 200,
            'data': [{'access_token': access_token,
                      'refresh_token': refresh_token,
                      'user': user
                     }]
            }

class RefreshToken(Resource):
    """
    Creates a refresh token and returns it as response to a
    post request from a client.
    """

    @jwt_refresh_token_required
    def post(self):
        """
        Returns a new access token
        """
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {
            'status': 200,
            'data': [{'access_token': new_token
                     }]
            }

#
#
# API resource routing
#

api_bp.add_resource(SignUp, '/auth/signup', endpoint='signup')
api_bp.add_resource(Login, '/auth/login', endpoint='login')
api_bp.add_resource(RefreshToken, '/auth/refresh', endpoint='refresh')
