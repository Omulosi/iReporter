"""
app.helpers
~~~~~~~~~~~

Implements various helpers

"""

from app import mail
from flask import jsonify
from sendgrid.helpers.mail import Mail
from threading import Thread
from flask import current_app


def make_token_header(token):
    """
    creates an authorization header given a
    token
    """
    return {'Authorization': 'Bearer {}'.format(token)}

def raise_error(status_code, message):
    """
    Returns a template for generating a custom error message
    """
    response = jsonify({"status": status_code,
                        "error": message})
    response.status_code = status_code
    return response

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(subject, sender, recipients, body):
    """
    A function for sending an email using sendgrid API
    """
    message = Mail(
        from_email=sender,
        to_emails=recipients,
        subject=subject,
        html_content='<p>{}</p>'.format(body))
    Thread(target=send_async_email,
        args=(current_app._get_current_object(), message)).start()
    mail.send(message)