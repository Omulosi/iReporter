"""
    app.api.v1.models
    ~~~~~~~~~~~~~~~~~~

    This module implements a database model used for storing and
    retrieving data using classes, lists and dictionaries.

"""

from datetime import datetime
import copy
#from flask_restful import fields

class Model:
    """
    Base class for all database objects
    """
    data_id = 0
    _db = {} # Represents the internal storage structure

    def __init__(self):
        self.created = datetime.utcnow()

    @classmethod
    def by_id(cls, item_id):
        """
        Returns an item given an id
        """
        return cls._db.get(item_id)

    @classmethod
    def all(cls):
        """
        Returns all items as a list collection
        of dictionary elements
        """
        db_copy = copy.deepcopy(cls._db)
        return [v.serialize for _, v in db_copy.items()]

    @classmethod
    def put(cls, item):
        """
        Stores an item.
        The entry should be a Model
        """
        if not isinstance(item, Model):
            raise ValueError('Data item should be a Model object')
        cls._db[item.data_id] = item

    @classmethod
    def delete(cls, item_id):
        """
        Deletes an item from the internal database
        """
        try:
            del cls._db[item_id]
            return True
        except KeyError:
            return

    def add_field(self, field, data):
        """
        Adds a new field attribute
        """
        setattr(self, field, data)


class User(Model):
    """
    Stores all data related to a user
    """

    def __init__(self, fname, lname, username, othernames=None,
                 phone_number=None, email=None, is_admin=False):
        self.fname = fname
        self.lname = lname
        self.othernames = "" if othernames is None else othernames
        self.phone_number = "" if phone_number is None else phone_number
        self.email = "" if email is None else email
        self.is_admin = is_admin
        self.username = username
        Model.__init__(self)
        self.data_id = self.data_id + 1
        User.data_id = self.data_id

    @property
    def serialize(self):
        """
        Returns a dict represention of the data stored in the object
        """
        return {
            'id': self.data_id,
            'firstname': self.fname,
            'lastname': self.lname,
            'othernames': self.othernames,
            'phoneNumber': self.phone_number,
            'username': self.username,
            'email': self.email,
            'isAdmin': self.is_admin,
            'created': self.created.strftime('%a, %d %b %Y %H:%M %p'),
            'uri': self.uri if hasattr(self, 'uri')  else ''
            }


class Record(Model):
    """
    Stores all data related to a record
    """

    def __init__(self, location, comment, _type='red-flag', status=None, image=None,
                 video=None, user=None):
        self.type = _type
        self.location = location
        self.comment = comment
        self.status = 'Under Investigation' if status is None else status
        self.image = [] if image is None else image
        self.video = [] if video is None else video
        self.user = user # A database model of type User
        Model.__init__(self)
        self.data_id = self.data_id + 1
        Record.data_id = self.data_id

    @property
    def serialize(self):
        """
        Returns a dict representation of the data stored in
        Record object
        """
        return {
            'id': self.data_id,
            'createdOn': self.created.strftime('%a, %d %b %Y %H:%M %p'),
            'createdBy': 10 if self.user is None else self.user.data_id,
            'type': self.type,
            'location': self.location,
            'status': self.status,
            'Images': self.image,
            'Videos': self.video,
            'comment': self.comment,
            'uri': self.uri if hasattr(self, 'uri')  else ''
            }
