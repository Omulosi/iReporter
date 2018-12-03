"""
    app.api.v1.views
    ~~~~~~~~~~~~~~~~~

    Implements API endpoints

"""
from flask_restful import Resource, reqparse, url_for
from . import api_bp
from .models import Record
from .errors import raise_error

class RedflagListAPI(Resource):
    """
    Implements methods for creating a record and returning a collection
    of records.
    """

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('comment', type=str, required=True, help='comment not provided')
        self.parser.add_argument('location', type=str, required=True, help='location not provided')
        super(RedflagListAPI, self).__init__()

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
        data = self.parser.parse_args() # Dictionary of input data
        record = Record(location=data['location'],
                        comment=data['comment'])
        uri = url_for('v1.redflag', _id=record.data_id, _external=True)
        record.add_field('uri', uri)
        Record.put(record)
        output = {'status': 201,
                  'data': [{"id": record.data_id, "message": "Created a red-flag record"}]
                 }

        return output, 201, {'Location': uri}

class RedflagAPI(Resource):
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

class RedflagUpdateAPI(Resource):
    """
    Updates the location or comment field of red-flag record
    """
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('comment', type=str)
        self.parser.add_argument('location', type=str)
        super(RedflagUpdateAPI, self).__init__()

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
        data = self.parser.parse_args()
        if field == 'location':
            new_location = data.get('location')
            if new_location is not None:
                record.location = new_location
        elif field == 'comment':
            new_comment = data.get('comment')
            if new_comment is not None:
                record.comment = new_comment
        Record.put(record)
        output = {}
        output['status'] = 200
        output['data'] = [{"id": _id, "message": "Updated red-flag record's " + field}]
        return output, 200
#
# API resource routing
#

api_bp.add_resource(RedflagListAPI, '/red-flags', endpoint='redflags')
api_bp.add_resource(RedflagAPI, '/red-flags/<_id>', endpoint='redflag')
api_bp.add_resource(RedflagUpdateAPI, '/red-flags/<_id>/<field>', endpoint='update_redflag')
