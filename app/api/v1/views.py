"""
    app.api.v1.views
    ~~~~~~~~~~~~~~~~~

    Implements API endpoints

"""

from flask_restful import Resource, reqparse, abort, Api
from . import bp
from .models import Record

API = Api(bp)

class RedflagListAPI(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('type', type=str, required=True,
                help='record type not provided')
        self.parser.add_argument('comment', type=str, 
                help='comment not provided', default="")
        self.parser.add_argument('location', type=str,
                help='location not provided', default="")
        super(RedflagListAPI, self).__init__()

    def get(self):
        """
        Returns a collection of all red-flag records
        """
        out = {'status': 200,
                'data': []
                }
        return out

    def post(self):
        """
        Creates a new red-flag record
        """
        out = self.parser.parse_args() # Dictionary of input data
        return out, 201

class RedflagAPI(Resource):

    def get(self, _id):
        """
        Returns a single red-flag record
        """

        out = {'status': 200,
                'data': []
                }
        return out

    def delete(self, _id):
        """
        Deletes a red-flag record
        """
        
        out = {'status': 200,
                'data': []
                }
        return out

class RedflagUpdateAPI(Resource):
    """
    Updates a red-flag record
    """
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('type', type=str)
        self.parser.add_argument('comment', type=str)
        self.parser.add_argument('location', type=str)
        super(RedflagUpdateAPI, self).__init__()

    def patch(self, _id, field):
        """
        Updates a field of a red-flag record
        """
        out = self.parser.parse_args()
        return out, 201
#
# API resource routing
#

API.add_resource(RedflagListAPI, '/red-flags')
API.add_resource(RedflagAPI, '/red-flags/<int:_id>')
API.add_resource(RedflagUpdateAPI, '/red-flags/<int:_id>/<field>')
