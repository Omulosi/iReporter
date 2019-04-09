"""
    run.py

"""

from app import create_app, cli
from app.db import Model

app = create_app()
cli.register(app)
