"""
    app.api.v2.utilities
    ~~~~~~~~~~~~~~~~~~

    This module contains general utility functions

"""

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
    return password if len(password) > 5 else None


def update_createdon(data_item):
    """
    updates the createdon field's datetime data into
    a string representation of the date.
    Returns a new dictionary item with the field
    updated
    """
    data_item['createdon'] = data_item['createdon'].strftime('%a, %d %b %Y %H:%M %p')
    return data_item