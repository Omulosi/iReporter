"""
    app.api.utils
    ~~~~~~~~~~~~~~~~~~

    This module contains general utility functions that help
    in processing and validating input data

"""

import re
from flask import jsonify

EMAIL_PATTERN = re.compile(r'^.+@[\w]+\.[\w]+')
PASSWORD_PATTERN = re.compile(r'.{5,}')
COMMENT_PATTERN = re.compile(r'.{1,}')
USERNAME_PATTERN = re.compile(r"^[a-zA-Z][\w]{3,}")
STATUS_PATTERN = re.compile(r'^(resolved|unresolved|under investigation)$', re.IGNORECASE)

def valid_field(field, regex_pattern):
    """
    field -> str
    regex_pattern -> regular expression
    Returns field if valid else None
    """
    return field if regex_pattern.match(field) else None

def raise_error(status_code, message):
    """
    Returns a template for generating a custom error message
    """
    response = jsonify({"status": status_code,
                        "error": message})
    response.status_code = status_code
    return response

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
    return valid_field(comment, COMMENT_PATTERN)

def valid_status(status):
    """
    Returns True if status is one of Resolved, Investigation, Unresolved.
    Otherwise returns False
    """
    return valid_field(status, STATUS_PATTERN)

def valid_username(username):
    """
    Username is not valid if it is empty, is numeric only
    or is composed of whitespaces only.
    """
    return valid_field(username, USERNAME_PATTERN)

def valid_email(email):
    """
    Returns email if it is valid otherwise None
    """
    return valid_field(email, EMAIL_PATTERN)

def valid_password(password):
    """
    Returns password if valid else None
    """
    # password = password.strip()
    # return password if len(password) >= 5 else None
    return valid_field(password, PASSWORD_PATTERN)

def update_createdon(data_item):
    """
    updates the createdon field's datetime data into
    a string representation of the date.
    Returns a new dictionary item with the field
    updated
    """
    data_item['createdon'] = data_item['createdon'].strftime('%a, %d %b %Y %H:%M %p')
    return data_item

def make_token_header(token):
    """
    creates an authorization header given a
    token
    """
    return {'Authorization': 'Bearer {}'.format(token)}


def can_update(parser, field, data_validator):
    """
    checks if field is valid and thus can be updated.
    """
    data_parser = parser.parse_args(strict=True)
    new_data = data_parser.get(field)
    return data_validator(new_data)
