"""
app.helpers
~~~~~~~~~~~

Implements various helpers

"""


from flask_mail import Message
from app import mail
from flask import jsonify

def make_token_header(token):
    """
    creates an authorization header given a
    token
    """
    return {'Authorization': 'Bearer {}'.format(token)}

def send_email(subject, sender, recipients, body):
    """
    A function for sending an email
    """
    msg = Message(subject=subject, sender=sender, recipients=recipients)
    msg.body = body
    mail.send(msg)

def raise_error(status_code, message):
    """
    Returns a template for generating a custom error message
    """
    response = jsonify({"status": status_code,
                        "error": message})
    response.status_code = status_code
    return response
