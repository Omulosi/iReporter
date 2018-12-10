"""
    app.api.v2.incidents
    ~~~~~~~~~~~~~~~~~~~~

    Implements API endpoints

"""
from flask_restful import Resource, reqparse, url_for
from . import api_bp
from .models import Record, User
from .errors import raise_error

class CreateOrReturnIncidents(Resource):
    """
    Implements methods for creating a record and returning a collection
    of records.
    """
    def get(self, incident_type):
        return {'type': incident_type}
    
    def post(self, incident_type):
        return {'type': incident_type}

class SingleIncident(Resource):
    """
    Implements methods for manipulating a particular record
    """
    def get(self, incident_type, id):
        return {'type': incident_type, 'id': id}

    def delete(self, incident_type, id):
        return {'type': incident_type, 'id': id}

class UpdateSingleIncident(Resource):
    """
    Updates the location or comment field of red-flag record
    """
    def patch(self, incident_type, id, field):
        return {'type': incident_type, 'id': id, 'field': field}


# API resource routing
#

api_bp.add_resource(CreateOrReturnIncidents, '/<incident_type>', endpoint='incidents')
api_bp.add_resource(SingleIncident, '/<incident_type>/<id>', endpoint='incident')
api_bp.add_resource(UpdateSingleIncident, '/<incident_type>/<id>/<field>', endpoint='update_incident')
