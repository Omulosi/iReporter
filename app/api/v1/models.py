"""
    app.api.v1.models
    ~~~~~~~~~~~~~~~~~~

    This module implements a database model used for storing and
    retrieving data using classes, lists and dictionaries.

"""

from datetime import datetime
import psycopg2
from collections import OrderedDict
from instance.config import DatabaseConfig
import os
from werkzeug.security import generate_password_hash, check_password_hash



def connect(config):
    """Connect to the PostgreSQL database.  Returns a database connection."""
    host = config.HOSTNAME
    username = config.USERNAME 
    password = config.SECRET_KEY
    dbname = config.DATABASE
    return psycopg2.connect(
        "host={} user={} password={} dbname={}".format(
        host, username, password, dbname))

def create_record_table(config=DatabaseConfig):
    """
    Create tables in an existing DB
    """
    try:
        db = connect(config)
        c = db.cursor()


        command = (
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
            """
        )

        c.execute(command)

        # Make the changes to the database persistent
        db.commit()
        # Close communication with the database
    except Exception as e:
        return
    finally:
        c.close()
        db.close()

def create_user_table(config=DatabaseConfig):
    """
    Create tables in an existing DB
    """
    try:
        db = connect(config)
        c = db.cursor()


        command = (
            """
            CREATE TABLE user_s (
                id serial PRIMARY KEY,
                firstname varchar(30),
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

        c.execute(command)

        # Make the changes to the database persistent
        db.commit()
        # Close communication with the database
    except Exception as e:
        return
    finally:
        c.close()
        db.close()

#create_record_table()
#create_user_table()

class Model:
    """
    Base class for all database objects
    """
    # data_id = 0
    # _db = {} 

    def __init__(self):
        self.created = datetime.utcnow()
        
    @classmethod
    def create_table(cls):
        create_user_table()
        create_record_table()

    @classmethod
    def by_id(cls, item_id):
        """
        Returns an item [{}] given an id, otherwise []
        Assumes item_id is of type int
        """
       
        res = []
        db = connect(DatabaseConfig)
        with db:
            with db.cursor() as c:
                if cls == Record:
                    c.execute("select * from record_s where id = %s;", (item_id,))
                if cls == User:
                    c.execute("select * from user_s where id = %s;", (item_id,))
                data_one = c.fetchone()
                colnames = [desc[0] for desc in c.description]
                if data_one:
                    res = [zip(colnames, data_one)]
        db.close()
        return [dict(elem) for elem in res]

    @classmethod
    def all(cls):
        """
        Returns all items as a list collection or [] if empty list
        of dictionary elements
        db_type takes a string: 'records' or 'user'
        """
        res = []
        db = connect(DatabaseConfig)
        with db:
            with db.cursor() as c:
                if cls == Record:
                    c.execute("select * from record_s order by createdon desc")
                if cls == User:
                    c.execute("select * from user_s order by registered desc")

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
        assert isinstance(item, Model), "Item should be of type Model"
        try:
            db = connect(DatabaseConfig)
            c = db.cursor()
            data = item.serialize.items()
            fields = tuple([item[0] for item in data])
            values = tuple([item[1] for item in data])
            if cls == Record:
                sql = """
                        insert into record_s
                        (type, comment, location, status, Images, Videos, uri, createdOn, createdBy) 
                        values (%s,%s,%s,%s,%s,%s,%s,%s,%s)
                    """
                c.execute(sql, values)
            if cls == User:
                sql = """
                        insert into user_s
                        (firstname, lastname, othernames, phoneNumber, username, email, registered, isAdmin, uri) 
                        values (%s,%s,%s,%s,%s,%s,%s,%s,%s)
                    """
                c.execute(sql, values)
            db.commit()
        except Exception as e:
            return
        finally:
            c.close()
            db.close()
       
    @classmethod
    def delete(cls, item_id):
        """
        Deletes an item from the internal database.
        Return true on successful deletion or none
        """
        db = connect(DatabaseConfig)
        with db:
            with db.cursor() as c:
                if cls == Record:
                    c.execute("delete from record_s where id = %s", (item_id,))
                if cls == User:
                    c.execute("delete from user_s where id = %s", (item_id,))
        db.commit()
        db.close()
        
    @classmethod
    def update(cls, item_id, field, data):
        """
        Updates an item from the database.
        """
        db = connect(DatabaseConfig)
        with db:
            with db.cursor() as c:
                if cls == Record:
                    sql = "update record_s set {} = ".format(field)
                    c.execute( sql +" %s where id  = %s", (data, item_id))
                    print("I am a record")
                if cls == User:
                    sql = "update user_s set {} = ".format(field)
                    c.execute( sql +" %s where id  = %s", (data, item_id))
                    print("I am a user")

        db.commit()
        db.close()     
        
    @classmethod
    def clear_all(cls):
        """
        Removes all items from the database model
        """
        db = connect(DatabaseConfig)
        with db:
            with db.cursor() as c:
                if cls == Record:
                    c.execute("delete from record_s")
                if cls == User:
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
        d['createdBy'] = 10

        return d
            
class User(Model):

    def __init__(self, username, email, fname=None, lname=None, othernames=None, phoneNumber=None, isAdmin=False):
        self.username = username
        self.email = email
        self.password_hash = None
        self.fname = "" if fname is None else fname
        self.lname = "" if lname is None else lname
        self.othernames = "" if othernames is None else othernames
        self.phoneNumber = "" if phoneNumber is None else phoneNumber
        self.isAdmin = isAdmin
        Model.__init__(self)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def serialize(self):
        """
        Returns an ordered dict representation of the data stored in
        User object
        """
        d = OrderedDict()

        d['firstname'] = self.fname
        d['lastname'] = self.lname
        d['othernames'] = self.othernames
        d['phoneNumber'] = self.phoneNumber
        d['username'] = self.username
        d['email'] = self.email
        d['registered'] = self.created.strftime('%a, %d %b %Y %H:%M %p')
        d['isAdmin'] = self.isAdmin
        d['uri'] = self.uri if hasattr(self, 'uri')  else ''

        return 