"""
    app.api.v1.models
    ~~~~~~~~~~~~~~~~~~

    This module implements a database model used for storing and
    retrieving data using classes, lists and dictionaries.

"""

from datetime import datetime
import psycopg2
from collections import OrderedDict
import logging

host = 'localhost'
username = 'omulosi' 
password = 'secret'
dbname = 'test_db'


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect(
        "host={} user={} password={} dbname={}".format(
        host, username, password, dbname))

def create_tables():
    """
    Create tables in an existing DB
    """
    try:
        db = connect()
        c = db.cursor()


        commands = (
            """
            CREATE TABLE record_s (
                id serial PRIMARY KEY,
                status varchar(30) NOT NULL,
                type varchar(20) NOT NULL,
                location varchar(50) NOT NULL,
                createdOn timestamp NOT NULL,
                createdBy integer NOT NULL,
                Videos text[],
                Images text[],
                uri varchar(30),
                comment varchar(160) NOT NULL
            )
            """,

            """
            CREATE TABLE user_s (
                id serial PRIMARY KEY,
                firtname varchar(30),
                lastname varchar(30),
                othernames varchar(50),
                email varchar(50) NOT NULL,
                phoneNumber varchar(30),
                username varchar(30) NOT NULL,
                registered timestamp NOT NULL,
                uri varchar(30),
                isAdmin bool NOT NULL
            )
            """
        )

        for command in commands:
            c.execute(command)

        # Make the changes to the database persistent
        db.commit()
        # Close communication with the database
    except Exception as e:
        print(e)
    finally:
        c.close()
        db.close()

create_tables()

class Model:
    """
    Base class for all database models
    """
    
    def __init__(self):
        self.created = datetime.utcnow()

    @classmethod
    def by_id(cls, item_id, db_type):
        """
        Returns an item [{}] given an id, otherwise []
        Assumes item_id is of type int
        """
       res = []
        db = connect()
        with db:
            with db.cursor() as c:
                if db_type == 'records':
                    c.execute("select * from record_s where id = %s;", (item_id,))
                    print("I am a record")
                if db_type == 'user':
                    c.execute("select * from user_s where id = %s;", (item_id,))
                    print("I am a user")

                data_one = c.fetchone()
                colnames = [desc[0] for desc in c.description]
                if data_one:
                    res = [zip(colnames, data_one)]
        db.close()
        return [dict(elem) for elem in res]   

    @classmethod
    def all(cls, db_type):
        """
        Returns all items as a list of dicts or [] if no itemms
        db_type is a string: 'records' or 'user'
        """
        res = []
        db = connect()
        with db:
            with db.cursor() as c:
                if db_type == 'records':
                    c.execute("select * from record_s order by createdon desc")
                    print("I am a record")
                if db_type == 'user':
                    c.execute("select * from user_s order by createdon desc")
                    print("I am a user")

                data_all = c.fetchall()
                colnames = [desc[0] for desc in c.description]
                if data_all:
                    res = [zip(colnames, data) for data in data_all]
        db.close()
        return [dict(elem) for elem in res]  

    @classmethod
    def put(cls, item):
        """
        Stores an item.
        The entry should be a Model
        """
        try:
            db = connect()
            c = db.cursor()
            data = item.serialize.items()
            fields = tuple([item[0] for item in data])
            values = tuple([item[1] for item in data])
            sql = """
                    insert into record_s
                    (type, comment, location, status, Images, Videos, uri, createdOn, createdBy) 
                    values (%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """
            c.execute(sql, values)
            db.commit()
        except Exception as e:
            print(e)
        finally:
            c.close()
            db.close()
       
    @classmethod
    def delete(cls, item_id, db_type):
        """
        Deletes an item from the internal database.
        Return true on successful deletion or none
        """
        db = connect()
        with db:
            with db.cursor() as c:
                if db_type == 'records':
                    c.execute("delete from record_s where id = %s", (item_id,))
                    print("I am a record")
                if db_type == 'user':
                    c.execute("delete from record_s where id = %s", (item_id,))
                    print("I am a user")

        db.commit()
        db.close()
        
    @classmethod
    def update(cls, item_id, db_type, field, data):
        """
        Updates an item from the database.
        """
        db = connect()
        with db:
            with db.cursor() as c:
                if db_type == 'records':
                    sql = "update record_s set {} = ".format(field)
                    c.execute( sql +" %s where id  = %s", (data, item_id))
                    print("I am a record")
                if db_type == 'user':
                    c.execute("update user_s set %s = %s where id  = %s", (field, data, item_id))
                    print("I am a user")

        db.commit()
        db.close()     
        
    @classmethod
    def clear_all(cls, db_type):
        """
        Removes all items from the database model
        """
        db = connect()
        with db:
            with db.cursor() as c:
                if db_type == 'records':
                    c.execute("delete from record_s")
                if db_type == 'user':
                    c.execute("delete from user_s")

        db.commit()
        db.close() 


class Record(Model):
    """
    Stores all data related to a record
    """

    def __init__(self, location, comment, _type='red-flag', status=None, image=None,
                 video=None):
        self.type = _type
        self.location = location
        self.comment = comment
        self.status = 'Under Investigation' if status is None else status
        self.image = [] if image is None else image
        self.video = [] if video is None else video
        Model.__init__(self)


    @property
    def serialize(self):
        """
        Returns an ordered dict representation of the data stored in
        Record object
        """
        d = OrderedDict()
        d['type'] = self.type
        d['comment'] = self.comment
        d['location'] = self.location
        d['status'] = self.status
        d['Images'] = self.image
        d['Videos'] = self.video
        d['uri'] = self.uri if hasattr(self, 'uri')  else ''
        d['createdOn'] = self.created.strftime('%a, %d %b %Y %H:%M %p')
        d['createdBy'] = 11

        return d

class User(Model):

    def __init__(self, fname, lname, username, othernames=None, phoneNumber=None, email=None, isAdmin=False):
        self.fname = fname
        self.lname = lname
        self.othernames = othernames
        self.phoneNumber = phoneNumber
        self.email = "" if not email else email
        self.isAdmin = isAdmin
        self.username = username
        Model.__init__(self)

    @property
    def serialize(self):
        d = OrderedDict()
        return {
        'id': self.id,
        'firstname': self.fname,
        'lastname': self.lname,
        'othernames': self.othernames,
        'phoneNumber': self.phoneNumber,
        'username': self.username,
        'email': self.email,
        'isAdmin': self.isAdmin,
        'created': self.created.strftime('%a, %d %b %Y %H:%M %p'),

        }
     @property
    def serialize(self):
        """
        Returns an ordered dict representation of the data stored in
        User object
        """
        d = OrderedDict()

        d['firstname'] = self.type
        d['lastname'] = self.comment
        d['othernames'] = self.location
        d['phoneNumber'] = self.status
        d['username'] = self.username
        d['email'] = self.email
        d['registered'] = self.created.strftime('%a, %d %b %Y %H:%M %p')
        d['isAdmin'] = self.isAdmin
        d['uri'] = self.uri if hasattr(self, 'uri')  else ''

        return d
            

