"""
    app.api.v2.errors
    ~~~~~~~~~~~~~~~~~

    Implement utility methods for handling error conditions

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
    return raise_error(422, error_msg)

@jwt.unauthorized_loader
def unauthorized_callback(error_msg):
    return raise_error(401, error_msg)

@jwt.expired_token_loader
def expired_token_callback():
    return raise_error(401, "Token has expired")
