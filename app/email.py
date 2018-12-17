"""

    Function for sending an email

"""

from flask_mail import Message
from app import mail

def send_email(subject, sender, recipients, text_body):
    """
    A function for sending an email
    """
    msg = Message(subject=subject, sender=sender, recipients=recipients)
    msg.body = text_body
    mail.send(msg)
