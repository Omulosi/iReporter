"""
    app.api.v1.views
    ~~~~~~~~~~~~~~~~~

    Implements API endpoints

"""
from flask_restful import Resource, reqparse, url_for
from . import api_bp
from .database import get_by_id, get_all, put_item, delete_item, update_item, connect, Record
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

    @jwt_required
    def get(self):
        """
        Returns a collection of all red-flag records
        """
        records = get_all('redflag')
        output = {'status': 200, 'data': records}
        return output

    @jwt_required
    def post(self):
        """
        Creates a new red-flag record
        """
        data = self.parser.parse_args() # Dictionary of input data
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
        put_item(record)
        db = connect()
        with db:
            with db.cursor() as c:
                c.execute("select max(id) from records")
                _id = c.fetchone()[0]
        db.close()
        uri = url_for('v1.redflag', _id=_id)
        output = {'status': 201,
                  'data': [{"id": _id, "message": "Created a red-flag record"}]
                 }

        return output, 201, {'Location': uri}

class SingleRedflag(Resource):
    """
    Implements methods for manipulating a particular record
    """
    @jwt_required
    def get(self, _id):
        """
        Returns a single red-flag record
        """
        if not _id.isnumeric():
            return raise_error(404, "Invalid ID")
        _id = int(_id)
        record = get_by_id(_id)
        if not record:
            return raise_error(404, "Record record not found")
        output = {'status': 200,
                  'data': [record.serialize]
                 }
        return output
    @jwt_required
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
        delete_item(_idS)
        out = {}
        out['status'] = 200
        out['data'] = [{'id':_id, 'message': 'red-flag record deleted'}]
        return out

class UpdateSingleRedflag(Resource):
    """
    Updates the location or comment field of red-flag record
    """
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('comment', type=str)
        self.parser.add_argument('location', type=str)
        super(UpdateSingleRedflag, self).__init__()

    @jwt_required
    def patch(self, _id, field):
        """
        Updates a field of a red-flag record
        """
        if not _id.isnumeric():
            return raise_error(404, "Invalid ID")
        _id = int(_id)
        record = get_by_id(_id)
        if not record:
            return raise_error(404, "Record does not exist")
        data = self.parser.parse_args()
        if field == 'location':
            new_location = data.get('location')
            if new_location is not None:
                update_item(_id, 'location', new_location)
        elif field == 'comment':
            new_comment = data.get('comment')
            if new_comment is not None:
                update_item(_id, 'comment', new_comment)
        elif field == 'status':
            new_status = data.get('status')
            if new_status is not None:
                update_item(_id, 'status', new_status)
        put_item(Record)
        output = {}
        output['status'] = 200
        output['data'] = [{"id": _id, "message": "Updated red-flag record's " + field}]
        return output, 200
        
#
# API resource routing
#

api_bp.add_resource(CreateOrReturnRedflags, '/red-flags', endpoint='redflags')
api_bp.add_resource(SingleRedflag, '/red-flags/<_id>', endpoint='redflag')
api_bp.add_resource(UpdateSingleRedflag, '/red-flags/<_id>/<field>', endpoint='update_redflag')
