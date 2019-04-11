"""
    app.api.v2.incidents
    ~~~~~~~~~~~~~~~~~~~~

    Implements API endpoints

"""

from flask_restful import Resource, reqparse, url_for
from flask import current_app
from flask_jwt_extended import jwt_required, get_jwt_identity, fresh_jwt_required
from app.utils import (valid_location, valid_comment, valid_status,
                           update_createdon, raise_error)
from app.helpers import send_email
from . import api_bp
from app.models import Record, User


#: create incident parser
create_incident_parser = reqparse.RequestParser()
create_incident_parser.add_argument('comment', type=str, required=True, help='comment not provided')
create_incident_parser.add_argument('location', type=str, required=True, help='location not provided')


class Incidents(Resource):
    """
    Implements methods for creating a record or returning a collection
    of records.
    """

    @fresh_jwt_required
    def post(self, incident_type, _id=None):
        """
        Creates a new incident record
        """
        if _id is not None:
            return raise_error(405, 'Method not allowed for the requested URL')
        #: Initialize database access objects
        USER = User()
        RECORD = Record()

        if incident_type not in ('red-flags', 'interventions'):
            return raise_error(404, "The requested url cannot be found")
        incident_type = incident_type[:-1]

        data = create_incident_parser.parse_args(strict=True)
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
        user_id = USER.filter_by('username', current_user)[0].get('id')

        record = RECORD.add(location=data['location'], comment=data['comment'],
                        _type=incident_type, user_id=int(user_id))
        record_id = RECORD.get_last_inserted_id()
        uri = url_for('v2.incidents',
                      incident_type=incident_type + 's', _id=record_id, _external=True)
        RECORD.update(record_id, 'uri', uri)

        output = {}
        output['id'] = record_id
        output["message"] = "Created {} record".format(incident_type)
        output = {'status': 201,
                  'data': [output],
                  'uri': uri
                 }

        return output, 201, {'Location': uri}

    @jwt_required
    def get(self, incident_type, _id=None):
        """
        Returns a single incident record
        """
        #: Initialize database access objects
        USER = User()
        RECORD = Record()

        if incident_type not in ('red-flags', 'interventions'):
            return raise_error(404, "The requested url cannot be found")

        if _id is None:
            incidents = RECORD.filter_by('type', incident_type[:-1])
            incidents = list(map(update_createdon, incidents))

            return {'status': 200,
                    'data': incidents
                   }
        print(_id)
        if not _id.isnumeric():
            return raise_error(400, "Invalid ID. Should be an Integer")

        incident_id = int(_id)
        incident_type = incident_type[:-1] # Remove the last 's' from name
        incident = RECORD.filter_by('id', incident_id)
        if not incident or incident[0]['type'] != incident_type:
            return raise_error(404, "{} not found".format(incident_type))

        incident = update_createdon(incident[0])

        output = {'status': 200,
                  'data': incident
                 }
        return output

    @fresh_jwt_required
    def delete(self, incident_type, _id):
        """
        Deletes a single incident record
        """

        #: Initialize database access objects
        USER = User()
        RECORD = Record()

        if not _id.isnumeric():
            return raise_error(400, "ID should be an integer")

        username = get_jwt_identity()
        user = USER.filter_by('username', username)[0]
        user_id = user.get('id')

        if incident_type not in ('red-flags', 'interventions'):
            return raise_error(404, "The requested url cannot be found")

        incident = RECORD.filter_by('id', _id)
        if not incident:
            return raise_error(404, "{} does not exist".format(incident_type))

        createdby = incident[0].get('createdby')
       
        if user_id != createdby:
            return raise_error(403, "You can only delete your own record.")

        RECORD.delete(_id)
        message = incident_type + ' has been deleted'

        output = {}
        output['status'] = 200
        output['data'] = [{'id':_id, 'message': message}]
        return output

class UpdateIncident(Resource):
    """
    Updates the location, comment or status field of an incident
    """

    @fresh_jwt_required
    def patch(self, incident_type, _id, field):
        """
        Updates the specified field (location, comment or status)
        """

        #: Initialize database access objects
        USER = User()
        RECORD = Record()

        if not _id.isnumeric():
            return raise_error(400, "ID should be an integer")
        if field not in ('location', 'comment', 'status'):
            return raise_error(400, "Invalid field name")

        #: Initialize a parser to collect user input
        parser = reqparse.RequestParser()
        parser.add_argument(field, type=str, required=True)

        #:
        #: Validate user input
        #:

        try:
            data = parser.parse_args(strict=True)
        except:
            error_msg = "Invalid input data. Only {} field should be provided".format(field)
            return raise_error(400, error_msg)

        new_field_value = data.get(field)
        if field == 'location':
            new_field_value = valid_location(new_field_value)
            error_msg = ("Invalid location. Either it is empty,"
                         "does not conform to 'lat, long' format"
                         "or exceeds valid ranges(+/- 90, +/- 180)")
        elif field == 'comment':
            new_field_value = valid_comment(new_field_value)
            error_msg = 'comment field should not be empty'
        elif field == 'status':
            new_field_value = valid_status(new_field_value)
            error_msg = ("Invalid status type. Status is either empty or "
                         "is not one of 'resolved','under investigation' or"
                         " 'unresolved' ")
        if not new_field_value:
            return raise_error(400, error_msg)

        #: Get incident record to be updated
        incident = RECORD.filter_by('id', _id)
        if not incident:
            return raise_error(404, "{} does not exist".format(incident_type[:-1]))
        createdby = incident[0].get('createdby')

        #: Get ID of user accessing endpoint
        username = get_jwt_identity()
        user = USER.filter_by('username', username)[0]
        user_id = user.get('id')
        
        #: Check for pemissions
        if field != 'status' and user_id != createdby:
            return raise_error(403, "You can only update {} field of "
                                    "your own record.".format(field))
        if field == 'status' and not user.get('isadmin'):
            return raise_error(403, "Request forbidden")

        #: All relevant checks have passed by this stage, update appropriate field
        RECORD.update(_id, field, new_field_value)

        output = {}
        msg = "Updated " + incident_type + " record's " + field
        output['status'] = 200
        output['data'] = [{"id": _id, "message": msg}]

        if field == 'status':
            user_email = user.get('email')
            if user_email:
                msg = msg + ' to ' + new_field_value
                send_email(subject="Status Update",
                           sender=current_app.config.get('MAIL_USERNAME'),
                           recipients=[user_email],
                           body=msg)
                
        return output