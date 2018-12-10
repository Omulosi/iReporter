"""
    app.api.v2.models
    ~~~~~~~~~~~~~~~~~~

    Database models for users and intervention records

"""

import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify
from funcy import project


class Base(db.Model):

    @classmethod
    def filter_by(cls, field, value):
        res = []
        if cls == Record:
            query = """ select * from records where {} = %s;""".format(field)
        if cls == User:
            query = """ select * from users where {} = %s;""".format(field)
        cls.query(query, (value,))
        items = cls.fetchall()
        fields = [desc[0] for desc in cls.cursor.description 
                  if desc[0] != 'user_id' if desc[0] != 'password_hash']
        if items:
            res = [zip(fields, item) for item in items]
        return [dict(elem) for elem in res]

    @classmethod
    def by_id(cls, item_id):
        res = []
        if cls == Record:
            query = "select * from records where id = %s;"
        if cls == User:
            query = "select * from users where id = %s;"
        cls.query(sql, (item_id,))
        item = cls.fetchall()
        fields = [desc[0] for desc in cls.cursor.description 
                   if desc[0] != 'user_id' if desc[0] != 'password_hash']
        if item:
            res = [zip(fields, item)]
        return [dict(elem) for elem in res]

    @classmethod
    def all(cls):
        res = []
        if cls == Record:
            items = cls.get_all('records')
        if cls == User:
            items = cls.get_all('users')
        fields = [desc[0] for desc in cls.cursor.description if desc[0] != 'user_id'
                  if desc[0] != 'password_hash']
        if items:
            res = [zip(fields, item) for item in items]
        return [dict(elem) for elem in res]



class Record(Base):
    """Record model"""
    def __init__(self, location, comment, type, user_id, status=None, createdBy=None,
                 Images=None, Videos=None, uri=None):
            #super(Record, self).__init__()
            self.location = location
            self.comment = comment
            self.type = type
            self.createdOn  =datetime.utcnow()
            self.user_id = user_id
            self.status = 'Under Investigation' if status is None else status
            self.createdBy = 0 if createdBy is None else createdBy
            self.Images = [] if Images is None else Images
            self.Videos = [] if Videos is None else Videos
            self.uri = '' if uri is None else uri

    def put(self):
    	query = """insert into records 
                (location, comment, type, createdOn, user_id, status, createdBy, Images, Videos, uri)
    			 values (%(location)s, %(comment)s, %(type)s, %(createdOn)s, %(user_id)s, %(status)s,
                 %(createdBy)s, %(Images)s, %(Videos)s, %(uri)s);"""
    	self.query(query, {'location': self.location, 
    					 'comment': self.comment,
    					 'type':  self.type,
    					 'createdOn': self.createdOn,
                         'user_id': self.user_id,
                         'status': self.status,
                         'createdBy': self.createdBy,
                         'Images': self.Images,
                         'Videos': self.Videos,
                         'uri': self.uri})

    	self.commit()


class User(Base):
    """User model"""
    def __init__(self, username, password, email=None, fname=None, lname=None, othernames=None, phoneNumber=None, isAdmin=False):
        super(User, self).__init__()
        self.username = username
        self.password_hash = generate_password_hash(password)
        self.email = '' email if email is None else email
        self.registered  = datetime.utcnow()
        self.firstname = "" if fname is None else fname
        self.lastname = "" if lname is None else lname
        self.othernames = "" if othernames is None else othernames
        self.phoneNumber = "" if phoneNumber is None else phoneNumber
        self.isAdmin = isAdmin

    def put(self):
        """
        Store a user in the database
        """
        query = """insert into users 
                (username, password_hash, email, createdOn, firstname, lastname, othernames,
                phoneNumber, isAdmin)
                values (%(username)s, %(password_hash)s, %(email)s, %(registered)s,
                %(firstname)s, %(lastname)s, %(othernames)s, %(phoneNumber)s, %(isAdmin)s);"""
        self.query(query, {'username': self.username, 
                         'password_hash': self.password_hash,
                         'email':  self.email,
                         'registered': self.registered,
                         'firstname': self.firstname,
                         'lastname': self.lastname,
                         'othernames': self.othernames.
                         'phoneNumber': self.phoneNumber,
                         'isAdmin': self.isAdmin
                         })

        self.commit()

    def create_record(self, **kwargs):
        """
        Input - key-value pairs
        """
        user = self.by_username(self.username)
        user_id = user[0]
        record = Record(**kwargs, user_id=user_id)
        record.put()




