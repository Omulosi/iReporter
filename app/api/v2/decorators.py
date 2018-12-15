"""
    app.api.v2.decorators
    ~~~~~~~~~~~~~~~~~~~~~~

    Decorator utility functions

"""

import functools as ft
from flask_restful import request
from flask_jwt_extended import get_jwt_identity
from app.api.errors import raise_error
from .models import Record, User


def parse_request_url_data(url):
    """"
    Parses the request url to obtain the
    incident_type(red-flag/intervention), id and
    field that are passed in by the user when requesting
    a resource.
    """
    url_data = url[url.find('v2'):].split('/')
    try:
        _, incident_type, _id, field = url_data
    except ValueError:
        _, incident_type, _id, field = url_data + ['']

    if incident_type not in ['red-flags', 'interventions']:
        return raise_error(404, "The requested url cannot be found")
    incident_type = incident_type[:-1]
    if not _id.isnumeric():
        return raise_error(400, "Invalid ID")
    _id = int(_id)
    return (incident_type, _id, field)


def validate_before_update(func):
    """
    A decorator to validate input data for patch and
    delete enpoints
    """

    @ft.wraps(func)
    def wrapper(*args, **kwargs):
        """"
        Ensures that the request url and all input data are
        valid before they are processed.
        Raises an appropriate error if any of the data is not
        valid.
        """
        incident_type, _id, field = parse_request_url_data(request.path)

        username = get_jwt_identity()
        user = User.filter_by('username', username)[0]
        user_id = user.get('id')

        incident = Record.filter_by('id', _id)
        if not incident:
            return raise_error(404, "{} does not exist".format(incident_type))
        createdby = incident[0].get('createdby')
        if field:
            if field != 'status' and user_id != createdby:
                return raise_error(403, "You can only update {} field of "
                                        "your own record.".format(field))
            if field == 'status' and not user.get('isadmin'):
                return raise_error(403, "Request forbidden")
        elif user_id != createdby:
            return raise_error(403, "You can only delete your own record.")
        return func(*args, **kwargs)

    return wrapper
