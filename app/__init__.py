'''
    app
    -----------
    This module provides an application factory function for
    creating and configuring a flask app. 
'''

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from config import Config
from app.db import db

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
    db.init_app(app)

    from app.api.v1 import bp as api_v1
    app.register_blueprint(api_v1, url_prefix='/api/v1')

    from app.api.v2 import bp as api_v2
    app.register_blueprint(api_v2, url_prefix='/api/v2')

    with app.app_context():
        db.init_db()

    return app
