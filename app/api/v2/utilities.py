"""
    app.api.v2.utilities
    ~~~~~~~~~~~~~~~~~~

    This module contains general utility functions that help
    in processing and validating input data

"""

from flask_jwt_extended import get_jwt_identity
from flask_restful import request
from .models import Record, User
from .errors import raise_error
import functools as ft

import re

def valid_location(location):
    """
    validates location input
    """
    try:
        coordinates = location.split(',')
        assert len(coordinates) == 2
        latitude, longitude = [float(c) for c in coordinates]
        assert -90 < latitude <= 90
        assert -180 <= longitude <= 180
        return location
    except (AssertionError, ValueError):
        return None

def valid_comment(comment):
    """
    Removes white spaces from comment.
    """
    comment = comment.strip()
    return comment

def valid_status(status):
    """
    Returns True if status is one of Resolved, Investigation, Unresolved.
    Otherwise returns False
    """
    status = status.strip()
    if status not in ['resolved', 'under investigation', 'unresolved']:
        return None
    return status


def valid_username(username):
    """
    Username is not valid if it is empty, is not numeric
    or is composed of whitespaces only.
    """
    pattern = re.compile(r"^[a-zA-Z][\w]{3,}")
    return username if pattern.match(username) else None

def valid_email(email):
    """
    Returns email if it is valid otherwise None
    """
    pattern = re.compile(r'^.+@[\w]+\.[\w]+')
    return email if pattern.match(email) else None

def valid_password(password):
    """
    Returns password if valid else None
    """
    password = password.strip()
    return password if len(password) >= 5 else None


def update_createdon(data_item):
    """
    updates the createdon field's datetime data into
    a string representation of the date.
    Returns a new dictionary item with the field
    updated
    """
    data_item['createdon'] = data_item['createdon'].strftime('%a, %d %b %Y %H:%M %p')
    return data_item


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

        username = get_jwt_identity()
        user = User.filter_by('username', username)[0]
        user_id = user.get('id')

        path = request.path
        params = path.split('/')[3:]
        field = ''
        if len(params) == 3:
            incident_type, _id, field = params
        if len(params) == 2:
            incident_type, _id = params

        if incident_type not in ['red-flags', 'interventions']:
            return raise_error(404, "The requested url cannot be found")
        incident_type = incident_type[:-1]
        if not _id.isnumeric():
            return raise_error(404, "Invalid ID")
        _id = int(_id)
        incident = Record.filter_by('id', _id)
        if not incident:
            return raise_error(404, "{} does not exist".format(incident_type))
        createdby = incident[0].get('createdby')
        if field:
            if field != 'status' and user_id != createdby:
                return raise_error(403, "You can only update {} field of your own record.".format(field))
            if field == 'status' and not user.get('isadmin'):
                return raise_error(403, "Request forbidden")
        elif user_id != createdby:
            return raise_error(403, "You can only delete your own record.")
        return func(*args, **kwargs)

    return wrapper

