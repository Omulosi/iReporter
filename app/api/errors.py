"""
    app.api.errors
    ~~~~~~~~~~~~~~~~~

    Implements utility methods for handling error conditions

"""

from flask import jsonify
from app import jwt

def raise_error(status_code, message):
    """
    Returns a template for generating a custom error message
    """
    response = jsonify({"status": status_code,
                        "error": message})
    response.status_code = status_code
    return response

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
