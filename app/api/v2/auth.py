"""
    app.api.v2.auth
    ~~~~~~~~~~~~~~~~~

    Implements authentication and authorization functionality

"""

from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_refresh_token_required, get_jwt_identity,
                                jwt_required, get_raw_jwt)
from flask_restful import Resource, reqparse
from app.utils import (valid_email, valid_password, update_createdon, valid_username, raise_error)
from app.models import User, Blacklist
from . import api_bp

#:
#: Sign Up parser
#:
signup_parser = reqparse.RequestParser()
signup_parser.add_argument('username', type=str, required=True,
                         help='Please enter username and password')
signup_parser.add_argument('password', type=str, required=True,
                         help='Please enter username and password')
#: Optional fields
signup_parser.add_argument('email', type=str)
signup_parser.add_argument('phone', type=str)
signup_parser.add_argument('firstname', type=str)
signup_parser.add_argument('lastname', type=str)
signup_parser.add_argument('othernames', type=str)
signup_parser.add_argument('isadmin', type=str)

#:
#: Log In parser
#:
login_parser = reqparse.RequestParser()
login_parser.add_argument('username', type=str, required=True,
                    help='Please enter username and password')
login_parser.add_argument('password', type=str, required=True,
                    help='Please enter username and password')


class SignUp(Resource):
    """
    Implements endpoints for signing up a user
    """

    def post(self):
        """
        Registers a new user
        """

        USER = User()

        data = signup_parser.parse_args()
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
        if USER.filter_by('username', username):
            return raise_error(400, "Please use a different username")
        if email and not valid_email(email):
            return raise_error(400, "Invalid email format")
        if email and USER.filter_by('email', email):
            return raise_error(400, "Please use a different email")
        if not valid_password(password):
            return raise_error(400, "Invalid password. "
                               "Ensure the password is at least 5 characters long")
        USER.add(username=username, password=password, email=email, firstname=firstname,
                    lastname=lastname, othernames=othernames, phone_number=phone, isadmin=isadmin)
    
        access_token = create_access_token(identity=username, fresh=True)
        refresh_token = create_refresh_token(identity=username)

        return {
            'status': 201,
            'data': [{'access_token': access_token,
                      'refresh_token': refresh_token,
                      'user': USER.serialize
                     }]
            }, 201

class Login(Resource):
    """
    Implements login endpoint. The endpoint returns an access and
    a fresh token on successful request.
    """
    

    def post(self):
        """
        Logs in a user
        """
        USER = User()

        data = login_parser.parse_args()
        username = data.get('username')
        password = data.get('password')

        if username is None:
            return raise_error(400, "Missing 'username' in body")
        if password is None:
            return raise_error(400, "Missing 'password' in body")

        #: Get the user object -  a dictionary
        user = USER.by_username(username)
        p_hash = user.get('password_hash', '')

        #: validate password
        if not user or not USER.check_password(p_hash, password):
            return raise_error(401, "Invalid username or password")

        #: create tokens
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
    Generates new access tokens given a refresh token
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

class LogoutAccess(Resource):
    """
    Revoke access tokens
    """

    @jwt_required
    def delete(self):
        """
        Revokes the current user's access token by storing it in
        the blacklist table
        """
        BLACLIST = Blacklist()

        # jti: json token identifier (unique identifier)
        jti = get_raw_jwt()['jti']
        BLACLIST.add(jti=jti)
    
        return {
            "status": 200,
            "message":"successfully logged out"
            }

class LogoutRefresh(Resource):
    """
    Revoke refresj tokens
    """

    @jwt_refresh_token_required
    def delete(self):
        """
        Revokes the current user's refresh token
        """

        BLACLIST = Blacklist()

        # jti: json token identifier
        jti = get_raw_jwt()['jti']

        #: store jti in the database
        BLACLIST.add(jti=jti)
        
        return {
            "status": 200,
            "message":"successfully logged out"
            }
