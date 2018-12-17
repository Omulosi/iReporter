"""
    app.db
    ~~~~~~~~~~~

    Provides interface methods for connecting to and manipulating the database.

"""

import psycopg2
from psycopg2.extras import RealDictCursor
from instance.config import Config

class Model(object):
    """
    Represents base database model that connects the
    database and provides some common utility
    functionalities for interacting with it
    """

    # db_url = "dbname='{}' user='{}' host='{}' password='{}'".format(
    #     Config.DBNAME, Config.USERNAME, Config.HOST, Config.PASSWORD)
    db_url = "dbname='testdb' user='jp' host='localhost' password='cavier'"


    conn = psycopg2.connect(db_url)
    # create a psycopg2 cursor that can execute queries
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    @classmethod
    def close_connection(cls):
        """
        closes the db connection
        """
        cls.conn.close()

    @classmethod
    def commit(cls):
        """
        commits the transaction to persist changes in the database
        """
        cls.conn.commit()

    @classmethod
    def query(cls, sql, params=None):
        """
        generic query method
        """
        cls.cursor.execute(sql, params or ())


    @classmethod
    def fetchall(cls):
        """
        fetches all data
        """
        return cls.cursor.fetchall()

    @classmethod
    def fetchone(cls):
        """
        fetches a single data item
        """
        cls.cursor.fetchone()

    @classmethod
    def by_username(cls, username):
        """
        Returns a user data item with the given username
        as a dictionary.
        """
        query = """ select * from users where username = %s;"""
        cls.query(query, (username,))
        record = cls.fetchall()
        return record[0] if record else {}

    @classmethod
    def comments(cls):
        """
        Returns list containing all comments each in a dictionary
        format.
        """
        sql = "select comment from records order by createdon desc;"
        cls.query(sql)
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
            createdon timestamp with time zone not null default now(),
            images varchar(120)[] not null,
            videos varchar(120)[] not null,
            uri varchar(140),
            createdby integer not null,
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
            username varchar(80) not null,
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
    def create_blacklist_table(cls):
        """
        Create the blacklist table
        """
        cls.cursor.execute("""create table if not exists blacklist (
            id serial primary key,
            jti varchar(140) not null
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
        cls.cursor.execute("""delete from blacklist;""")
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
        cls.cursor.execute("""drop table records;""")
        cls.cursor.execute("""drop table users;""")
        cls.cursor.execute("""drop table blacklist;""")
        cls.commit()

    @classmethod
    def create_all_tables(cls):
        """
        Deletes all tables
        """
        cls.create_users_table()
        cls.create_records_table()
        cls.create_blacklist_table()

    @classmethod
    def drop_table(cls, table_name):
        """
        Deletes a specific table given the table name
        """
        query = """drop table {};""".format(table_name)
        cls.cursor.execute(query)
        cls.commit()

    @classmethod
    def rollback(cls):
        """
        Abstracts commit command of the database's cursor
        """
        cls.cursor.execute("rollback;")
        cls.commit()
