"""
app.db.db
~~~~~~~~~~~

Functiond for setting up the database

"""

import click
from flask import current_app, g
from flask.cli import with_appcontext
import psycopg2
from config import Config


def get_db():
    
    if 'db' not in g:
        g.db = psycopg2.connect(
                current_app.config['DATABASE']
                )

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def create_records():
    
    query = """
            create table if not exists records (
            id serial primary key,
            type varchar(50) not null,
            comment varchar(140) not null,
            location varchar(30) not null,
            status varchar(50) not null,
            createdon timestamp with time zone not null default now(),
            images varchar(120)[] not null,
            videos varchar(120)[] not null,
            uri varchar(140),
            createdby integer not null,
            user_id integer references users(id) on delete cascade not null
            );
        """

    db = get_db()
    with db:
        with db.cursor() as cursor:
            cursor.execute(query)

def create_users():

    query = """
            create table if not exists users (
            id serial primary key,
            username varchar(80) not null,
            email varchar(100) not null,
            createdOn timestamp with time zone not null,
            firstname varchar(100) not null,
            lastname varchar(100) not null,
            othernames varchar(100) not null,
            phoneNumber varchar(100) not null,
            isAdmin boolean not null,
            password_hash varchar(100) not null
            );"""

    db = get_db()
    with db:
        with db.cursor() as cursor:
            cursor.execute(query)

def create_blacklist():
    query = """
            create table if not exists blacklist (
            id serial primary key,
            jti varchar(140) not null
            );"""

    db = get_db()
    with db:
        with db.cursor() as cursor:
            cursor.execute(query)

def init_db():
    # db = get_db()

    # with current_app.open_resource('db/schema.sql') as f:
    #     with db.cursor() as cursor:
    #         cursor.execute(f.read().decode('utf8'))

    create_records()
    create_users()
    create_blacklist()


def clear_tables():
    db = get_db()
    with db:
        with db.cursor() as cursor:
            cursor.execute("""delete from users;""")
            cursor.execute("""delete from records;""")
            cursor.execute("""delete from blacklist;""")
        db.commit()

def rollback():
    db = get_db()
    with db:
        with db.cursor() as cursor:
            cursor.execute("rollback;")
        db.commit()

#: Database cli commands
@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database')

@click.command('clear-all-db')
@with_appcontext
def clear_all_db_command():
    """clear all tables."""
    clear_tables()
    click.echo('All tables cleared')

@click.command('rollback-db')
@with_appcontext
def rollback_db_command():
    """Rollback previous transaction."""
    rollback()
    click.echo('Transaction rolled back')


# Register above commands with the application
def init_app(app):
    # call close_db when cleaning up after returning a response
    app.teardown_appcontext(close_db)
    # add a new command that can be called with flask command
    app.cli.add_command(init_db_command)
    app.cli.add_command(rollback_db_command)
    app.cli.add_command(clear_all_db_command)
