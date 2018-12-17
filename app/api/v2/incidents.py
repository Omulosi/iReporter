"""
    app.api.v2.incidents
    ~~~~~~~~~~~~~~~~~~~~

    Implements API endpoints

"""

from flask_restful import Resource, reqparse, url_for
from flask_jwt_extended import jwt_required, get_jwt_identity, fresh_jwt_required
from app.api.utils import (valid_location, valid_comment, valid_status,
                           update_createdon, raise_error, can_update)
from app.email import send_email
from . import api_bp
from .models import Record, User
from .decorators import validate_before_update

class CreateOrReturnIncidents(Resource):
    """
    Implements methods for creating a record or returning a collection
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
        incidents = list(map(update_createdon, incidents))
        return {'status': 200,
                'data': incidents
               }

    @fresh_jwt_required
    def post(self, incident_type):
        """
        Creates a new incident record
        """
        if incident_type not in ['red-flags', 'interventions']:
            return raise_error(404, "The requested url cannot be found")
        incident_type = incident_type[:-1]
        data = self.parser.parse_args(strict=True)
        location = data.get('location')
        comment = data.get('comment')
        if not valid_location(location):
            return raise_error(400, "Invalid location. Check that the location field"
                                    "is not empty and that it has a 'lat,long' format"
                                    "and is within valid ranges (+/-90, +/-180).")
        if not valid_comment(comment):
            return raise_error(400, "Invalid  comment. Check that the comment "
                                    "is not empty/blank and that it has meaningful words")
        current_user = get_jwt_identity()
        user_id = User.filter_by('username', current_user)[0].get('id')
        record = Record(location=data['location'], comment=data['comment'],
                        _type=incident_type, user_id=int(user_id))
        record.put()
        record_id = Record.get_last_inserted_id()
        uri = url_for('v2.incident',
                      incident_type=incident_type + 's', _id=record_id, _external=True)
        Record.update(record_id, 'uri', uri)
        output = {}
        output['id'] = record_id
        output["message"] = "Created {} record".format(incident_type)
        output = {'status': 201,
                  'data': [output],
                  'uri': uri
                 }

        return output, 201, {'Location': uri}

class SingleIncident(Resource):
    """
    Implements methods for manipulating a particular record with a given id.
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
        incident = update_createdon(incident[0])
        output = {'status': 200,
                  'data': incident
                 }
        return output

    @fresh_jwt_required
    @validate_before_update
    def delete(self, incident_type, _id):
        """
        Deletes a single incident record
        """
        Record.delete(_id)
        message = incident_type + ' has been deleted'
        output = {}
        output['status'] = 200
        output['data'] = [{'id':_id, 'message': message}]
        return output

class UpdateSingleIncident(Resource):
    """
    Updates the location, comment or status field of an incident
    """

    def __init__(self):
        self.location_parser = reqparse.RequestParser()
        self.comment_parser = reqparse.RequestParser()
        self.status_parser = reqparse.RequestParser()
        self.location_parser.add_argument('location', type=str, required=True,
                                          help='location not provided')
        self.comment_parser.add_argument('comment', type=str, required=True,
                                         help='comment not provided')
        self.status_parser.add_argument('status', type=str, required=True,
                                        help='status not provided')
        super(UpdateSingleIncident, self).__init__()


    @fresh_jwt_required
    @validate_before_update
    def patch(self, incident_type, _id, field):
        """
        Updates the specified field (location, comment or status)
        """

        if field == 'location':
            error_msg = ("Invalid location. Either it is empty,"
                         "does not conform to 'lat, long' format"
                         "or exceeds valid ranges(+/- 90, +/- 180)")
            parser, data_validator = self.location_parser, valid_location

        elif field == 'comment':
            error_msg = 'comment field should not be empty'
            parser, data_validator = self.comment_parser, valid_comment

        elif field == 'status':
            error_msg = ("Invalid status type. Status is either empty or "
                         "is not one of 'resolved','under investigation' or"
                         " 'unresolved' ")
            parser, data_validator = self.status_parser, valid_status

        new_data = can_update(parser, field, data_validator)
        if not new_data:
            return raise_error(400, error_msg)
        Record.update(_id, field, new_data)
        output = {}
        msg = "Updated " + incident_type + " record's " + field
        output['status'] = 200
        output['data'] = [{"id": _id, "message": msg}]
        if field == 'status':
            record = Record.by_id(int(_id))
            u_id = record[0].get('createdby')
            user = User.by_id(u_id)[0]
            user_email = user.get('email')
            msg = msg + ' to ' + new_data
            if user_email:
                send_email("Status Update", 'mulongojohnpaul@gmail.com', [user_email], msg)
        return output

class ReturnUserIncidents(Resource):
    """
    Implements methods for manipulating a particular record
    """

    @jwt_required
    def get(self, user_id, incident_type):
        """
        Return all incidents (red-flag/intervention) created by
        a paricular with the id 'user_id'.
        """
        if incident_type not in ['red-flags', 'interventions']:
            return raise_error(404, "The requested url cannot be found")
        incident_type = incident_type[:-1]
        if not user_id.isnumeric():
            return raise_error(404, "Invalid ID. Should be an Integer")
        user_id = int(user_id)
        if not User.by_id(user_id):
            return raise_error(404, "User does not exist")

        incidents = Record.query("""select * from records where user_id = %s and
                type = %s;""", (user_id, incident_type))
        incidents = Record.fetchall()
        incidents = list(map(update_createdon, incidents))
        return {'status': 200,
                'data': incidents
               }

# API resource routing
#

api_bp.add_resource(CreateOrReturnIncidents, '/<incident_type>', endpoint='incidents')
api_bp.add_resource(SingleIncident, '/<incident_type>/<_id>', endpoint='incident')
api_bp.add_resource(UpdateSingleIncident, '/<incident_type>/<_id>/<field>',\
        endpoint='update_incident')
api_bp.add_resource(ReturnUserIncidents, '/users/<user_id>/<incident_type>',
                    endpoint='user_incidents')
