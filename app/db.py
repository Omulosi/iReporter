"""
    app.db
    ~~~~~~~~~~~

    connects to the database and provides interface methods to interact with
    the database.

"""
import psycopg2
from instance.config import Config

class Model(object):

    """
    Base class for database management methods
    """

    connect_str = "dbname='{}' user='{}' host='{}' password='{}'".format(
    	   Config.DBNAME, Config.USERNAME, Config.HOST, Config.PASSWORD)
    # use our connection values to establish a connection
    conn = psycopg2.connect(connect_str)
    # create a psycopg2 cursor that can execute queries
    cursor = conn.cursor()

    @classmethod
    def close_connection(cls):
        """ closes the  db connection """

        cls.conn.close()

    @classmethod
    def commit(cls):
        """
        Abstracts commit command of the database's cursor
        """
        cls.conn.commit()

    @classmethod
    def rollback(cls):
        """
        Abstracts commit command of the database's cursor
        """
        cls.cursor.execute("rollback;")
        cls.commit()

    @classmethod
    def query(cls, query, params=None):
        """
        Generic query method
        """

        cls.cursor.execute(query, params or ())

    @classmethod
    def fetchall(cls):
        """
        Abstracts fetchall command of the database's cursor
        """
        cls.cursor.fetchall()

    @classmethod
    def fetchone(cls):
        """
        Abstracts fetchone command of the database's cursor
        """
        return cls.cursor.fetchone()[0]

    @classmethod
    def by_username(cls, username):
        """
        Returns a db item that matches username
        """
        query = "select * from users where username = '{}';".format(username)
        cls.query(query)
        return cls.fetchall()

    @classmethod
    def comments(cls):
        """
        Returns all comments stored in records table
        """
        sql = "select comment from records order by createdOn desc;"
        cls.query(sql)
        return cls.fetchall()


    @classmethod
    def get_all(cls, table_name, *params):
        """
        Takes a table_name(str) and params(tuple of fields).
        Returns a collection of all items
        """
        if not params:
            query = "select * from {} order by createdOn desc;".format(table_name)
        else:
            columns = ','.join([p for p in params])
            query = query = "select {} from {} order by createdOn desc;".format(columns, table_name)
        cls.query(query)
        return cls.fetchall()

    @classmethod
    def create_records_table(cls):
        """
        Create the records table
        """
        cls.cursor.execute("""create table if not exists records (
            id serial primary key,
            type varchar(50) not null,
            comment varchar(140) not null,
            location varchar(30) not null,
            status varchar(50) not null,
            createdOn timestamp with time zone not null,
            Images bytea[],
            Videos bytea[],
            uri varchar(140),
            user_id integer references users(id) on delete cascade not null
            );
            """)
        cls.commit()

    @classmethod
    def create_users_table(cls):
        """
        Create the users table
        """
        cls.cursor.execute("""create table if not exists users (
            id serial primary key,
            username varchar(80) unique not null,
            email varchar(100) not null,
            createdOn timestamp with time zone not null,
            firstname varchar(100) not null,
            lastname varchar(100) not null,
            othernames varchar(100) not null,
            phoneNumber varchar(100) not null,
            isAdmin boolean not null,
            password_hash varchar(100) not null
            );
            """)
        cls.commit()

    @classmethod
    def clear_all_tables(cls):
        """
        Clears all tables
        """
        cls.cursor.execute("""delete from records;""")
        cls.cursor.execute("""delete from users;""")
        cls.commit()

    @classmethod
    def clear_table(cls, table_name):
        """
        Clears a specific table given the table name
        """
        query = """delete from {};""".format(table_name)
        cls.cursor.execute(query)
        cls.commit()

    @classmethod
    def drop_all_tables(cls):
        """
        Deletes all tables
        """
        cls.cursor.execute("""drop table records if exists;""")
        cls.cursor.execute("""drop table users if exists;""")
        cls.commit()

    @classmethod
    def drop_table(cls, table_name):
        """
        Deletes a specific table given the table name
        """
        query = """drop table {};""".format(table_name)
        cls.cursor.execute(query)
        cls.commit()
