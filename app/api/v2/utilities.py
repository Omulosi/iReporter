"""
    app.api.v2.utilities
    ~~~~~~~~~~~~~~~~~~

    General utility functions used for validating inputs

"""

import re

def valid_location(location):
    """
    validates location input
    """
    try:
        coords_list_str = location.split(',')
        assert len(coords_list_str) == 2
        latitude, longitude = [float(c) for c in coords_list_str]
        assert -90 < latitude <= 90
        assert -180 <= longitude <= 180
        return location
    except (AssertionError, ValueError):
        return None

def valid_comment(comment):
    """
    Removes white spaces from comment
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
    pattern = re.compile(r'^.+@[\w]+\.[\w]+')
    return email if pattern.match(email) else None

def valid_password(password):
    password = password.strip()
    return password if len(password) > 5 else None