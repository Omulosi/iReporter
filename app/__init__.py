"""
    app
    ~~~~

    A flask application that implements a RESTful API  for the iReporter
    application.

"""

from flask import Flask
from instance.config import Config

def create_app(config_class=Config):
    """
    An application factory function for creating a flask app
    instance and registering blueprints
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    from app.api.v1 import bp as api_v1
    app.register_blueprint(api_v1, url_prefix='/api/v1')

    return app
