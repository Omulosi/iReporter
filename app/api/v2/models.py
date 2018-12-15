# """
#     app.api.v2.models
#     ~~~~~~~~~~~~~~~~~~

#     Database models for users and intervention records

# """



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
        Takes a field by which to filter and returns all items
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
    def delete(cls, _id, user_id=None):
        """
        Deletes a record
        """
        if cls == Record and user_id:
            query = "delete from records where id=%s and user_id=%s;"
            cls.query(query, (_id, user_id))
        if cls == User and not user_id:
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

    @classmethod
    def get_last_inserted_id(cls):
        """ Given field(string) and data,
        updates field with data
        """
        table = 'records' if (cls == Record) else 'users'
        query = "select id from {} order by id desc limit 1;".format(table)
        cls.query(query)
        _id = cls.fetchall()
        return _id


class Record(Base):

    """Record model"""

    def __init__(self, location, comment, _type, user_id=None, status=None, images=None,
                 videos=None, uri=None):
        self.location = location
        self.comment = comment
        assert _type in ['red-flag', 'intervention'], "Wrong incident type.\
                Use 'red-flag' or 'intervention'"
        self.type = _type
        self.createdon = datetime.utcnow()
        self.user_id = user_id or ''
        self.status = staus or 'Draft'
        self.images = images or []
        self.videos = videos or []
        self.uri = uri or ''

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
                    'createdOn': self.createdon,
                    'user_id': self.user_id,
                    'status': self.status,
                    'Images': self.images,
                    'Videos': self.videos,
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
            'createdOn': self.createdon.strftime('%a, %d %b %Y %H:%M %p'),
            'createdBy': self.user_id,
            'type': self.type,
            'location': self.location,
            'status': self.status,
            'Images': self.images,
            'Videos': self.videos,
            'comment': self.comment,
            'uri': self.uri
            }


class User(Base):

    """User model"""

    def __init__(self, username, password, email=None, firstname=None, lastname=None,
                 othernames=None, phone_number=None, isadmin=None):
        super(User, self).__init__()
        self.username = username
        self.password_hash = generate_password_hash(password)
        self.email = email or ''
        self.registered = datetime.utcnow()
        self.firstname = firstname or ''
        self.lastname = lastname or ''
        self.othernames = othernames or ''
        self.phone_number = phone_number or ''
        self.isadmin = isadmin or False

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
                           'phoneNumber': self.phone_number,
                           'isAdmin': self.isadmin
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
            'phoneNumber': self.phone_number,
            'isAdmin': self.isadmin
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
    def check_password(password_hash, password):
        """
        Returns True if password hash is valid
        False otherwise.
        """
        return check_password_hash(password_hash, password)
