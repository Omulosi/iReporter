'''
	app.api.v2.users
	------------------

	API endpoints for for obtaining information about
	the current user and for listing all registered users
'''
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import User as USER_MODEL
from app.decorators import admin_required
from app.utils import update_createdon


class User(Resource):
    """
    Endpoints for obtaining info about current user
    """

    @jwt_required
    def get(self):
        """
         Returns info about current user'.
        """

        USER = USER_MODEL()

        user_identity = get_jwt_identity()
        user = USER.filter_by('username', user_identity)[0] # A list with user object

        data = update_createdon(user)

        return {'status': 200,
                'data': [data]
               }


class Users(Resource):
    """
    Endpoint for returning a list of all users
    """
    @admin_required
    @jwt_required
    def get(self):
        """
        Return a list of all users registered for
        the service.
        """
        USER = USER_MODEL()

        users = USER.all()

        return {'status': 200,
                'data': users
               }