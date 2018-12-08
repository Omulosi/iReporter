"""
    app.api.v1.views
    ~~~~~~~~~~~~~~~~~

    Implements API endpoints

"""
from flask_restful import Resource, reqparse, url_for
from . import api_bp
from .models import Record
from .errors import raise_error


def valid_location(location):
    try:
        coords_list_str = location.split(',')
        assert len(coords_list_str) == 2
        latitude, longitude = [float(c) for c in coords_list_str]
        assert -90 < latitude <= 90
        assert -180 <= longitude <= 180
        return location
    except (AssertionError, ValueError):
        return

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
        comment = data.get('comment')
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
        self.location_parser.add_argument('location', type=str)
        self.comment_parser.add_argument('comment', type=str)
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
            location_data = self.location_parser.parse_args(strict=True)
            new_location = location_data.get('location')
            if not new_location:
                return raise_error(400, 'location field should not be empty')
            if not valid_location(new_location):
                return raise_error(400, 'location field has invalid format')
            record.location = new_location
            
        elif field == 'comment':
            comment_data = self.comment_parser.parse_args(strict=True)
            new_comment = comment_data.get('comment')
            if not new_comment:
                return raise_error(400, 'comment field should not be empty')
            record.comment = new_comment
        Record.put(record)
        output = {}
        output['status'] = 200
        output['data'] = [{"id": _id, "message": field + ' has been successfully updated'}]
        return output, 200
#
# API resource routing
#

api_bp.add_resource(CreateOrReturnRedflags, '/red-flags', endpoint='redflags')
api_bp.add_resource(SingleRedflag, '/red-flags/<_id>', endpoint='redflag')
api_bp.add_resource(UpdateSingleRedflag, '/red-flags/<_id>/<field>', endpoint='update_redflag')
