"""
    app
    ~~~~

    A flask application that implements a RESTful API  for the iReporter
    application.

"""

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from instance.config import Config

jwt = JWTManager()
mail = Mail()

def create_app(config_class=Config):
    """
    An application factory function for creating a flask app
    instance and registering blueprints
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    jwt.init_app(app)
    mail.init_app(app)

    from app.api.v1 import bp as api_v1
    app.register_blueprint(api_v1, url_prefix='/api/v1')

    from app.api.v2 import bp as api_v2
    app.register_blueprint(api_v2, url_prefix='/api/v2')

    return app
