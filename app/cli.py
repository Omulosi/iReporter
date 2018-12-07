
from instance.config import Config
import os 
import click


host = Config.HOSTNAME
username = Config.USERNAME 
dbname = Config.DATABASE 
password = Config.SECRET_KEY


def register(app):
    @app.cli.group()
    def db():
        """Database management commands"""
        pass

    @db.command():
    def init():
        """
        Create the tables to be used by the appplication.
        """

        db = psycopg2.connect(database=dname,
                              username=username,
                              password=password,
                              host=host,
                              port='5432')
        with db:
            with db.cursor() as c:
                # Create new tabels
                c.execute('drop table if exists users')
                c.execute('drop table if exists records')

                # Create new tables
                commands = (
                """
                CREATE TABLE IF NOT EXISTS records (
                    id serial PRIMARY KEY,
                        status varchar(30) NOT NULL,
                        type varchar(20) NOT NULL,
                        location varchar(50) NOT NULL,
                        createdOn timestamp NOT NULL,
                        createdBy integer NOT NULL,
                        Videos text[],
                        Images text[],
                        comment varchar(160) NOT NULL
                    )
                    """,

                    """CREATE TABLE IF NOT EXISTS users(
                         user_id serial PRIMARY KEY NOT NULL,
                         first_name varchar(50) ,
                         last_name varchar(50),
                         user_name varchar(50) NOT NULL,
                         email varchar(50) NOT NULL,
                         password varchar(50) NOT NULL,
                         registered timestamp with time zone DEFAULT ('now'::text)::date NOT NULL,
                         isAdmin character varying(100) DEFAULT 'false' NOT NULL
                   )"""
                )

                for command in commands:
                    c.execute(command)

            db.close()


    @db.commad()
    def drop_tables():
        """
        Drop all tables and start afresh.
        """
        db = psycopg2.connect(database=dname,
                              username=username,
                              password=password,
                              host=host,
                              port='5432')

        with db:
            with db.cursor() as c:
                c.execute("drop table users")
                c.execute("drop table records")




import click
from app import create_app

app = create_app()

@click.group()
def db():
    """ Create Tables"""
    pass

@click.command()
def init_db():
    click.echo('ffffffd')

cli.add_argument(init_db)

if name == '__main__':
    cli()