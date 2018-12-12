"""
    app.api.v2.models
    ~~~~~~~~~~~~~~~~~~

    Database models for users and intervention records

"""

from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import db


class Base(db.Model):
    """
    Implements common query methods shared by User and Record classes
    """

    @classmethod
    def filter_by(cls, field, value):
        """
        field -> str
        Takes a field by which to filter and returns an item
        with the field specified
        """
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
    def all(cls):
        """
        Return all items from users or records
        """
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

    @classmethod
    def by_id(cls, item_id):
        """
        Query an item by id
        """
        res = []
        if cls == Record:
            query = "select * from records where id = %s;"
        if cls == User:
            query = "select * from users where id = %s;"
        cls.query(query, (item_id,))
        item = cls.fetchall()
        if item:
            fields = [desc[0] for desc in cls.cursor.description if desc[0] != 'user_id'
                      if desc[0] != 'password_hash']
            res = [dict(zip(fields, item))]
        return res

    @classmethod
    def delete(cls, _id):
        """
        Deletes a record
        """
        if cls == Record:
            query = "delete from records where id=%s;"
        if cls == User:
            query = "delete from users where id=%s;"
        cls.query(query, (_id,))

    @classmethod
    def update(cls, _id, field, data):
        """ Given field(string) and data,
        updates field with data
        """
        if cls == Record:
            query = "update records set {} = ".format(field)
        if cls == User:
            query = "update users set {} = ".format(field)
        cls.query(query + " %s where id = %s", (data, _id))


class Record(Base):

    """Record model"""

    def __init__(self, location, comment, _type, user_id=None, status=None, Images=None,
                 Videos=None, uri=None):
        self.location = location
        self.comment = comment
        assert _type in ['red-flags', 'interventions'], "Wrong incident type.\
                Use 'red-flags' or 'incidents'"
        self.type = _type
        self.createdOn = datetime.utcnow()
        self.user_id = "" if user_id is None else user_id
        self.status = 'Under Investigation' if status is None else status
        self.Images = [] if Images is None else Images
        self.Videos = [] if Videos is None else Videos
        self.uri = '' if uri is None else uri

    def put(self):
        """
        Store the an item in the database
        """

        query = """insert into records (location, comment, type, createdOn, user_id, status,
        Images, Videos, uri) values (%(location)s, %(comment)s, %(type)s,
        %(createdOn)s, %(user_id)s, %(status)s, %(Images)s, %(Videos)s,
        %(uri)s);"""

        self.query(query,
                {
                    'location': self.location,
                    'comment': self.comment,
                    'type': self.type,
                    'createdOn': self.createdOn,
                    'user_id': self.user_id,
                    'status': self.status,
                    'Images': self.Images,
                    'Videos': self.Videos,
                    'uri': self.uri
                })
        self.commit()

    @property
    def serialize(self):
        """
        Returns a dict representation of the data stored in
        Record object
        """
        return {
            'createdOn': self.createdOn.strftime('%a, %d %b %Y %H:%M %p'),
            'createdBy': self.user_id,
            'type': self.type,
            'location': self.location,
            'status': self.status,
            'Images': self.Images,
            'Videos': self.Videos,
            'comment': self.comment,
            'uri': self.uri
            }


class User(Base):

    """User model"""

    def __init__(self, username, password, email=None, fname=None, lname=None,
                 othernames=None, phoneNumber=None, isAdmin=False):
        super(User, self).__init__()
        self.username = username
        self.password_hash = generate_password_hash(password)
        self.email = '' if email is None else email
        self.registered = datetime.utcnow()
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
                           'othernames': self.othernames,
                           'phoneNumber': self.phoneNumber,
                           'isAdmin': self.isAdmin
                          })

        self.commit()

    @property
    def serialize(self):
        """
        Returns a dict representation of the data stored in
        Record object
        """
        return {
            'registered': self.registered.strftime('%a, %d %b %Y %H:%M %p'),
            'username': self.username,
            'email': self.email,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'othernames': self.othernames,
            'phoneNumber': self.phoneNumber,
            'isAdmin': self.isAdmin
            }

    def create_record(self, **kwargs):
        """
        Input - key-value pairs
        """
        user = self.by_username(self.username)
        user_id = user[0]
        record = Record(user_id=user_id, **kwargs)
        record.put()

    @staticmethod
    def check_password(p_hash, password):
        """
        Returns True if password hash is valid
        False otherwise.
        """
        return check_password_hash(p_hash, password)

