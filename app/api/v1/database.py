"""
    app.api.v1.models
    ~~~~~~~~~~~~~~~~~~

    This module implements a database model used for storing and
    retrieving data using classes, lists and dictionaries.

"""

from datetime import datetime
from collections import OrderedDict
import os
from werkzeug.security import generate_password_hash, check_password_hash
from instance.config import Config
import psycopg2


host = Config.HOSTNAME
username = Config.USERNAME 
dname = Config.DATABASE 
password = Config.SECRET_KEY


def connect():
    return psycopg2.connect(database=dname,user=username,password=password,host=host,port='5432')


def get_by_id(item_id):
    """
    Returns an item [{}] given an id, otherwise []
    Assumes item_id is of type int
    """
    res = []
    db = connect()
    with db:
        with db.cursor() as c:
            c.execute("select * from records where id = %s;", (item_id,))
            data_one = c.fetchone()
            colnames = [desc[0] for desc in c.description]
            if data_one:
                res = [zip(colnames, data_one)]
    db.close()
    return [dict(elem) for elem in res]

def get_all(_type=None):
    res = []
    db = connect()
    with db:
        with db.cursor() as c:
            if _type is None:
                 c.execute("select * from records order by createdOn desc", (_type,))
            else:
                c.execute("select * from records where type = %s order by createdOn desc", (_type,))
            data_all = c.fetchall()
            colnames = [desc[0] for desc in c.description]
            if data_all:
                res = [zip(colnames, data) for data in data_all]
    db.close()
    return [dict(elem) for elem in res] 
 
def put_item(item):
    """
    Stores an item.
    """
    try:
        db = connect()
        c = db.cursor()
        data = item.serialize.items()
        fields = tuple([item[0] for item in data])
        values = tuple([item[1] for item in data])
        print(fields)
        print(values)
        if isinstance(item, Record):
            c.execute("""
                    insert into records
                    (type, comment, location, status, Images, Videos, createdBy, createdOn) 
                    values (%s,%s,%s,%s,%s,%s,%s, %s);
                    """,
                    values)
            db.commit()
        if isinstance(item, User):
            c.execute("""
                    insert into users
                    (firstname, lastname, othernames, phoneNumber, username, email, isAdmin, registered, password_hash) 
                    values (%s,%s,%s,%s,%s,%s,%s,%s, %s);
                     """,
                values)
            db.commit()
    except Exception as e:
        return
    finally:
        c.close()
        db.close()
  
def delete_item(item_id):
    """
    Deletes an item from the database.
    Return true on successful deletion or none
    """
    db = connect()
    with db:
        with db.cursor() as c:
            c.execute("delete from records where id = %s", (item_id,))
    db.commit()
    db.close()

def update_item(item_id, field, data):
    """
    Updates an item from the database.
    """
    db = connect()
    with db:
        with db.cursor() as c:
            sql = "update records set {} = ".format(field)
            c.execute( sql +" %s where id  = %s", (data, item_id))
    db.commit()
    db.close()     
    
def clear_db():
    """
    Removes all items from the database model - users and records
    """
    db = connect()
    with db:
        with db.cursor() as c:
            c.execute("delete from users;")
            c.execute("delete from users;")

    db.commit()
    db.close() 

def get_by_username(username):
    """
    Returns a user given a field
    """
    res = []
    db = connect()
    with db:
        with db.cursor() as c:
            c.execute("select * from users where username = %s;", (userna,))
            data_one = c.fetchone()
    db.close()
    if data_one:
        return data_one

def get_by_email(email):
    """
    Returns a user given a field
    """
    res = []
    db = connect()
    with db:
        with db.cursor() as c:
            c.execute("select * from users where email = %s;", (email,))
            data_one = c.fetchone()
    db.close()
    if data_one:
        return data_one


#
# Storage containers for user input
#


class Model(object):

    def __init__(self):
        self.created = datetime.utcnow()
        
class Record(object):
    """
    Stores all data related to a record
    """

    def __init__(self, location, comment, _type=None, status=None, image=None,
                 video=None):
        self.type = 'red-flag' if _type is None else _type
        self.location = location
        self.comment = comment
        self.status = 'Under Investigation' if status is None else status
        self.image = [] if image is None else image
        self.video = [] if video is None else video
        #Model.__init__(self)


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
        d['createdBy'] = 10
        #d['createdOn'] = self.created.strfime("%A, %d. %B %Y %I:%M%p")
        return d
            
class User(object):

    def __init__(self, username, email=None, fname=None, lname=None, othernames=None, phoneNumber=None, isAdmin=False):
        self.username = username
        self.email = "" if email is None else email
        self.password_hash = None
        self.fname = "" if fname is None else fname
        self.lname = "" if lname is None else lname
        self.othernames = "" if othernames is None else othernames
        self.phoneNumber = "" if phoneNumber is None else phoneNumber
        self.isAdmin = isAdmin
        #Model.__init__(self)

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
        d['email'] = self.email,
        d['isAdmin'] = self.isAdmin,
        d['password_hash'] = self.password_hash
        #d['registered'] = self.created.strfime("%A, %d. %B %Y %I:%M%p")

        return 

def check_password(password):
        return check_password_hash(password_hash, password)