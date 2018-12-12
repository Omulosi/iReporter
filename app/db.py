"""
    app.db
    ~~~~~~~~~~~

    connects to the database and provides interface methods to interact with
    the database.

"""
import psycopg2
from instance.config import Config

class Model(object):

    connect_str = "dbname='{}' user='{}' host='{}' password='{}'".format(
    	Config.DBNAME, Config.USERNAME, Config.HOST, Config.PASSWORD)
    # use our connection values to establish a connection
    conn = psycopg2.connect(connect_str)
    # create a psycopg2 cursor that can execute queries
    cursor = conn.cursor()

    @classmethod
    def close_connection(cls):
        cls.conn.close()

    @classmethod
    def commit(cls):
        cls.conn.commit()

    @classmethod
    def query(cls, sql, params=None):
        cls.cursor.execute(sql, params or ())


    @classmethod
    def fetchall(cls):
        return cls.cursor.fetchall()

    @classmethod
    def fetchone(cls):
        cls.cursor.fetchone()

    @classmethod
    def by_username(cls, username):
        query = "select * from users where username = %s;"
        cls.query(query, (username,))
        return cls.fetchall()

    @classmethod
    def comments(cls):
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
            query = query = "select {} from {} order by createdOn desc;".format(columns,table_name)
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
            createdOn timestamp with time zone not null default now(),
            Images not null,
            Videos not null,
            uri varchar(140),
            user_id integer references users(id) on delete cascade not null;
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
        cls.cursor.execute("""drop table records;""")
        cls.cursor.execute("""drop table users;""")
        cls.commit()

    @classmethod
    def drop_table(cls, table_name):
        """
        Deletes a specific table given the table name
        """
        query = """drop table {};""".format(table_name)
        cls.cursor.execute(query)
        cls.commit()