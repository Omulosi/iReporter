"""
    app.api.v2.errors
    ~~~~~~~~~~~~~~~~~

"""

from flask import jsonify

def raise_error(status_code, message):
    """
    Returns a template for generating a custom error message
    """
    response = jsonify({"status": status_code,
                        "error": message})
    response.status_code = status_code
    return response
