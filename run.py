from app import create_app, cli
import click

app = create_app()
cli.register(app)
