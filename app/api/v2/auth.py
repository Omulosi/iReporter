"""
    app.api.v2.auth
    ~~~~~~~~~~~~~~~~~

    Implements authentication and authorization functionality (Sign In and Sign Up)

"""

from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_refresh_token_required, get_jwt_identity)
from flask_restful import Resource, reqparse, url_for
from . import api_bp
from .models import Record, User
from .errors import raise_error
from werkzeug.security import check_password_hash

class SignUp(Resource):
    """
    Implements method for signing up a suser
    """
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username', type=str, required=True, 
                help='Please enter username and password')
        self.parser.add_argument('password', type=str, required=True,
                help='Please enter username and password')
        self.parser.add_argument('email', type=str)
        super(SignUp, self).__init__()

    def post(self):
        data = self.parser.parse_args()
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')

        access_token = create_access_token(identity=username, fresh=True)
        refresh_token = create_refresh_token(identity=username)

        return {
            'status': 201,
            'data': [{'access_token': access_token,
                      'refresh_token': refresh_token,
                      'user': {'username': username}
                     }]
            }, 201


class Login(Resource):
    """
    Implements login endpoint. The endpoint returns and access and
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
        data = self.parser.parse_args()
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')

        access_token = create_access_token(identity=username, fresh=True)
        refresh_token = create_refresh_token(identity=username)

        return {
            'status': 200,
            'data': [{'access_token': access_token,
                      'refresh_token': refresh_token,
                      'user': {'username': username}
                     }]
            }

class RefreshToken(Resource):
    """
    Creates a refresh token and returns it as response to a
    post request from a client.
    """

    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        new_refresh_token = create_access_token(identity=current_user, fresh=False)
        return {
            'status': 200,
            'data': [{'access_token': new_refresh_token
                     }]
            }

#
#
# API resource routing
#

api_bp.add_resource(SignUp, '/auth/signup', endpoint='signup')
api_bp.add_resource(Login, '/auth/login', endpoint='login')
api_bp.add_resource(RefreshToken, '/auth/refresh', endpoint='refresh')
