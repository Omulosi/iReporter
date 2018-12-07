"""
    app.api.v1.views
    ~~~~~~~~~~~~~~~~~

    Implements API endpoints

"""
from flask_restful import Resource, reqparse, url_for
from . import api_bp
from .database import get_by_id, get_all, put_item, delete_item, update_item, connect, Record
from .errors import raise_error
from flask_jwt_extended import jwt_required


class CreateOrReturnInterventions(Resource):
    """
    Implements methods for creating a record and returning a collection
    of records.
    """

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('comment', type=str, required=True, help='comment not provided')
        self.parser.add_argument('location', type=str, required=True, help='location not provided')
        super(CreateOrReturnInterventions, self).__init__()
    @jwt_required
    def get(self):
        """
        Returns a collection of all red-flag records
        """
        records = get_all('intervention')
        output = {'status': 200, 'data': records}
        return output
    @jwt_required
    def post(self):
        """
        Creates a new red-flag record
        """
        data = self.parser.parse_args() # Dictionary of input data
        record = Record(location=data['location'],
                        comment=data['comment'], _type='intervention')
        put_item(record)
        
        #uri = url_for('v1.interventions', _id=_id, _external=True)
        output = {'status': 201,
                  'data': [{"id": _id, "message": "Created an intervention record"}]
                 }

        return output, 201, {'Location': uri}

class SingleIntervention(Resource):
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
        record = get_by_id(_id)
        if not record:
            return raise_error(404, "Record does not exist")
        delete_item(_id)
        out = {}
        out['status'] = 200
        out['data'] = [{'id':_id, 'message': 'intervention record deleted'}]
        return out

class UpdateSingleIntervention(Resource):
    """
    Updates the location or comment field of red-flag record
    """
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('comment', type=str)
        self.parser.add_argument('location', type=str)
        super(UpdateSingleIntervention, self).__init__()
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
        output = {}
        output['status'] = 200
        output['data'] = [{"id": _id, "message": "Updated Intervention record's " + field}]
        return output, 200
        
#
# API resource routing
#

api_bp.add_resource(CreateOrReturnInterventions, '/interventions', endpoint='interventions')
api_bp.add_resource(SingleIntervention, '/interventions/<_id>', endpoint='single_intervention')
api_bp.add_resource(UpdateSingleIntervention, '/interventions/<_id>/<field>', endpoint='update_intervention')
