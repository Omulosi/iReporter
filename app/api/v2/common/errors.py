"""
    app.api.v2.errors
    ~~~~~~~~~~~~~~~~~

    contains functions for handling error conditions

"""

from app import jwt
from app.utils import raise_error
from app.models import Blacklist
from .. import bp

@jwt.invalid_token_loader
def invalid_token_callback(error_msg):
    """
    Returns a custom 422 error message when a user
    provides an invalid token
    """
    return raise_error(422, error_msg)

@jwt.unauthorized_loader
def unauthorized_callback(error_msg):
    """
    Called when invalid credentials are provided
    """
    return raise_error(401, error_msg)

@jwt.expired_token_loader
def expired_token_callback():
    """
    Returns a custom error message when a user provides
    an expired token
    """
    return raise_error(401, "Token has expired")

@jwt.revoked_token_loader
def revoked_token_callback():
    """
    Returns a custom error message when a user provides
    a revoked token
    """
    return raise_error(401, "Token has been revoked")
