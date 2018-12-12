"""
    app.cli
    ~~~~~~~~~~~

    Provides convenience commands for manipulating the database

"""

import click
from app.db import Model

def register(app):
    @app.cli.group()
    def db():
        """
        Database management commands
        """
        pass

    @db.command()
    def create_records():
        """
        Create a new records table if one does not exist
        """
        Model.create_records_table()


    @db.command()
    def create_users():
        """
        Create a new users table if one does not exist
        """
        Model.create_users_table()

    @db.command()
    def create_all():
        """
        Creates both a users table and a records table
        """
        Model.create_users_table()
        Model.create_records_table()

    @db.command()
    def clear_all():
        """
        Clear all existing tables. (users and records)
        """
        Model.clear_all_tables()

    @db.command()
    @click.argument('name')
    def clear_table(name):
        """
        Clear a specific table given table name
        """
        Model.clear_table(name)

    @db.command()
    def drop_all():
        """
        Delete all existing tables. (users and records)
        """
        Model.drop_all_tables()

    @db.command()
    @click.argument('name')
    def drop_table(name):
        """
        Delete a specific table given table name
        """
        Model.drop_table(name)

    @db.command()
    def close_db():
        """
        Closes the database connection
        """
        Model.close_connection()
