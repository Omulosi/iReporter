"""
    app.api.v1.views
    ~~~~~~~~~~~~~~~~~

    Implements API endpoints

"""
from flask_restful import Resource, reqparse, url_for
from . import api_bp
from .models import Record
from app.utils import valid_location, valid_comment, can_update, raise_error

#
# Input validation functions
#

class CreateOrReturnRedflags(Resource):
    """
    Implements methods for creating a record and returning a collection
    of records.
    """

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('comment', type=str, required=True, help='comment not provided')
        self.parser.add_argument('location', type=str, required=True, help='location not provided')
        super(CreateOrReturnRedflags, self).__init__()

    def get(self):
        """
        Returns a collection of all red-flag records
        """
        records = Record.all()
        output = {'status': 200, 'data': Record.all()}
        return output

    def post(self):
        """
        Creates a new red-flag record
        """
        data = self.parser.parse_args(strict=True) # Dictionary of input data
        location = data.get('location')
        comment = data.get('comment').strip()
        if not location or not comment:
            return raise_error(400, "Neither location nor comment should be empty")
        location = valid_location(location)
        if location is None:
            return raise_error(400, "Wrong input format for location. "
                "Use 'lat, long' format. Ensure they are within a valid range")
        record = Record(location=data['location'],
                        comment=data['comment'])
        uri = url_for('v1.redflag', _id=record.data_id, _external=True)
        record.add_field('uri', uri)
        Record.put(record)
        output = {'status': 201,
                  'data': [record.serialize]
                 }

        return output, 201, {'Location': uri}

class SingleRedflag(Resource):
    """
    Implements methods for manipulating a particular record
    """

    def get(self, _id):
        """
        Returns a single red-flag record
        """
        if not _id.isnumeric():
            return raise_error(404, "Invalid ID")
        _id = int(_id)
        record = Record.by_id(_id)
        if record is None:
            return raise_error(404, "Record record not found")
        output = {'status': 200,
                  'data': [record.serialize]
                 }
        return output

    def delete(self, _id):
        """
        Deletes a red-flag record
        """

        if not _id.isnumeric():
            return raise_error(404, "Invalid ID")
        _id = int(_id)
        record = Record.by_id(_id)
        if record is None:
            return raise_error(404, "Record does not exist")
        Record.delete(_id)
        out = {}
        out['status'] = 200
        out['data'] = [{'id':_id, 'message': 'red-flag record deleted'}]
        return out

class UpdateSingleRedflag(Resource):
    """
    Updates the location or comment field of red-flag record
    """
    def __init__(self):
        self.location_parser = reqparse.RequestParser()
        self.comment_parser = reqparse.RequestParser()
        self.location_parser.add_argument('location', type=str, required=True)
        self.comment_parser.add_argument('comment', type=str, required=True)
        super(UpdateSingleRedflag, self).__init__()

    def patch(self, _id, field):
        """
        Updates a field of a red-flag record
        """
        if not _id.isnumeric():
            return raise_error(404, "Invalid ID")
        _id = int(_id)
        record = Record.by_id(_id)
        if record is None:
            return raise_error(404, "Record does not exist")
        if field == 'location':
            error_msg = 'location field invalid'
            parser, data_validator = self.location_parser, valid_location
        elif field == 'comment':
            error_msg = 'comment field should not be empty'
            parser, data_validator = self.comment_parser, valid_comment

        new_data = can_update(parser, field, data_validator)
        if not new_data:
            return raise_error(400, error_msg)
        Record.put(record)
        output = {}
        output['status'] = 200
        output['data'] = [{"id": _id, "message": field + ' has been successfully updated', "record": record.serialize }]
        return output, 200
#
# API resource routing
#

api_bp.add_resource(CreateOrReturnRedflags, '/red-flags', endpoint='redflags')
api_bp.add_resource(SingleRedflag, '/red-flags/<_id>', endpoint='redflag')
api_bp.add_resource(UpdateSingleRedflag, '/red-flags/<_id>/<field>', endpoint='update_redflag')
