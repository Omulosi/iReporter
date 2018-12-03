"""
    app.api.v1.errors
    ~~~~~~~~~~~~~~~~~

    Defines custom representations for API error messages.

"""

from flask import jsonify

def raise_error(status_code, message):
    """
    Returns a custom error message
    """
    response = jsonify({"status": status_code,
                        "error": message})
    response.status_code = status_code
    return response
