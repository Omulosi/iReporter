"""
    app.api.v2.incidents
    ~~~~~~~~~~~~~~~~~~~~

    Implements API endpoints

"""
from flask_restful import Resource, reqparse, url_for
from flask_jwt_extended import jwt_required, get_jwt_identity, fresh_jwt_required
from . import api_bp
from .models import Record, User
from .errors import raise_error
from .utilities import valid_location, valid_comment, valid_status

class CreateOrReturnIncidents(Resource):
    """
    Implements methods for creating a record and returning a collection
    of records.
    """

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('comment', type=str, required=True, help='comment not provided')
        self.parser.add_argument('location', type=str, required=True, help='location not provided')
        super(CreateOrReturnIncidents, self).__init__()

    @jwt_required
    def get(self, incident_type):
        """
        Returns a collection of either all redflags or
        all intervention records
        """
        if incident_type not in ['red-flags', 'interventions']:
            return raise_error(404, "The requested url cannot be found")
        incidents = Record.filter_by('type', incident_type[:-1])
        return {'status': 200,
                'data': str(incidents)
               }

    @fresh_jwt_required
    def post(self, incident_type):
        """
        Creates a new incident record
        """
        if incident_type not in ['red-flags', 'interventions']:
            return raise_error(404, "The requested url cannot be found")
        data = self.parser.parse_args(strict=True)
        location = data.get('location')
        comment = data.get('comment')
        if not valid_location(location) or not valid_comment(comment):
            error_msg = "Invalid location and/or comment fields. Check that both fields are not empty and that location has a 'lat,long' format and is within valid ranges."
            return raise_error(400,error_msg)
        current_user = get_jwt_identity()
        user = User.filter_by('username', current_user)
        user_id = user[0].get('id')
        record = Record(location=data['location'], comment=data['comment'], _type=incident_type[:-1],
            user_id=int(user_id))
        record.put()
        _id = Record.get_last_inserted_id()[0][0]
        uri = url_for('v2.incident', incident_type=incident_type, _id=_id,  _external=True)
        output = {}
        output['id'] = _id
        output["message"] = "Created intervention record"
        output = {'status': 201,
                  'data': [output],
                  'uri': uri
                 }

        return output, 201, {'Location': uri}

class SingleIncident(Resource):
    """
    Implements methods for manipulating a particular record
    """

    @jwt_required
    def get(self, incident_type, _id):
        """
        Returns a single incident record
        """
        if incident_type not in ['red-flags', 'interventions']:
            return raise_error(404, "The requested url cannot be found")
        if not _id.isnumeric():
            return raise_error(404, "Invalid ID. Should be an Integer")
        _id = int(_id)
        incident_type = incident_type[:-1]
        incident = Record.filter_by('id', _id)
        if not incident or incident[0]['type'] != incident_type:
            return raise_error(404, "{} not found".format(incident_type))
        incident = incident[0]
        incident['createdon'] = incident.get('createdon').strftime('%a, %d %b %Y %H:%M %p')
        output = {'status': 200,
                  'data': incident
                 }
        return output

    @fresh_jwt_required
    def delete(self, incident_type, _id):
        """
        Deletes a single incident record
        """
        if incident_type not in ['red-flags', 'interventions']:
            return raise_error(404, "The requested url cannot be found")
        if not _id.isnumeric():
            return raise_error(404, "Invalid ID")
        _id = int(_id)
        current_user = get_jwt_identity()
        user = User.filter_by('username', current_user)
        user_id = user[0].get('id')
        Record.delete(_id, user_id)
        msg = incident_type[:-1] + ' has been deleted'
        out = {}
        out['status'] = 200
        out['data'] = [{'id':_id, 'message': msg}]
        return out

class UpdateSingleIncident(Resource):
    """
    Updates the location, comment or status field of an incident
    """

    def __init__(self):
        self.location_parser = reqparse.RequestParser()
        self.comment_parser = reqparse.RequestParser()
        self.status_parser = reqparse.RequestParser()
        self.location_parser.add_argument('location', type=str, required=True)
        self.comment_parser.add_argument('comment', type=str)
        self.status_parser.add_argument('status', type=str)
        super(UpdateSingleIncident, self).__init__()

    @fresh_jwt_required
    def patch(self, incident_type, _id, field):
        """
        Updates the specified field (location, comment or status)
        """

        if incident_type not in ['red-flags', 'interventions']:
            return raise_error(404, "The requested url cannot be found")
        if not _id.isnumeric():
            return raise_error(404, "Invalid ID")
        _id = int(_id)
        if field == 'location':
            location_data = self.location_parser.parse_args(strict=True)
            new_location = location_data.get('location')
            if not valid_location(new_location):
                return raise_error(400, "Invalid location. Either it is empty, does not conform to 'lat, long' format or exceeds valid ranges(+/- 90, +/- 180)")
            Record.update(_id, field, new_location)

        elif field == 'comment':
            comment_data = self.comment_parser.parse_args(strict=True)
            new_comment = comment_data.get('comment')
            if not valid_comment(new_comment):
                return raise_error(400, 'comment field should not be empty')
            Record.update(_id, field, new_comment)

        elif field == 'status':
            username = get_jwt_identity()
            user = User.filter_by('username', username)
            if user and not user[0].get('isadmin'):
                return raise_error(403, "Request forbidden")
            status_data = self.status_parser.parse_args(strict=True)
            new_status = status_data.get('status')
            if not valid_status(new_status):
                error_msg = "Invalid status type. Input status is either empty or is not one of 'Resolved', 'Under Investigation' or 'Unresolved'" 
                return raise_error(400, error_msg)
            Record.update(_id, field, new_status)

        output = {}
        msg = "Updated " + incident_type[:-1] + " record's " + field
        output['status'] = 200
        output['data'] = [{"id": _id, "message": msg}]
        return output, 200


# API resource routing
#

api_bp.add_resource(CreateOrReturnIncidents, '/<incident_type>', endpoint='incidents')
api_bp.add_resource(SingleIncident, '/<incident_type>/<_id>', endpoint='incident')
api_bp.add_resource(UpdateSingleIncident, '/<incident_type>/<_id>/<field>',\
        endpoint='update_incident')
