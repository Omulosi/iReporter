'''
    app.models
    -----------------
    Database wrapper and models
'''


from datetime import datetime
from psycopg2.extras import RealDictCursor
from werkzeug.security import generate_password_hash, check_password_hash
from app.db.db import get_db

class Model:

    def __init__(self):
        #: Get the connection object
        self.conn = get_db()
        self.cursor = self.conn.cursor(cursor_factory=RealDictCursor)

    def commit(self):
        """
        commits the transaction to persist changes in the database
        """
        self.conn.commit()

    
    def query(self, sql, params=None):
        """
        generic query method
        """
        self.cursor.execute(sql, params or ())


    
    def fetchall(self):
        """
        fetches all data
        """
        return self.cursor.fetchall()

    
    def fetchone(self):
        """
        fetches a single data item
        """
        self.cursor.fetchone()

    
    def clear_all_tables(self):
        """
        Clears all tables
        """
        self.cursor.execute("""delete from records;""")
        self.cursor.execute("""delete from users;""")
        self.cursor.execute("""delete from blacklist;""")
        self.commit()

    
    def filter_by(self, field, value):
        """
        field -> str
        Takes a field and a value by which to filter
        Returns a list of all matching items as dictionaries
        in a list or an empty list
        """
        if isinstance(self, Record):
            query = """ select * from records where {} = %s;""".format(field)
        if isinstance(self, User):
            query = """ select * from users where {} = %s;""".format(field)
        self.query(query, (value,))
        return self.fetchall()

    
    def all(self):
        """
        Return all items from users or records as a list of
        dictionaries or an empty list
        """
        if isinstance(self, Record):
            query = """select * from records order by createdon desc;"""
        if isinstance(self, User):
            query = """select * from records order by createdon desc;"""
        self.query(query)
        return self.fetchall()

    
    def by_id(self, item_id):
        """
        Query an item by id
        """
        if isinstance(self, Record):
            query = "select * from records where id = %s;"
        if isinstance(self, User):
            query = "select * from users where id = %s;"
        self.query(query, (item_id,))
        return self.fetchall()

    
    def delete(self, _id):
        """
        Deletes a data item with the specified id.
        """
        if isinstance(self, Record):
            query = "delete from records where id=%s;"
        if isinstance(self, User):
            query = "delete from users where id=%s;"
        self.query(query, (_id,))
        self.commit()

    
    def update(self, _id, field, data):
        """
        Given a field(string) and data,
        updates field with data.
        """
        if isinstance(self, Record):
            query = "update records set {} = ".format(field)
        if isinstance(self, User):
            query = "update users set {} = ".format(field)
        self.query(query + " %s where id = %s", (data, _id))
        self.commit()

    
    def get_last_inserted_id(self):
        """ Given field(string) and data,
        updates field with data
        """
        table = 'records' if isinstance(self, Record) else 'users'
        query = "select id from {} order by id desc limit 1;".format(table)
        self.query(query)
        _id = self.fetchall()
        if _id:
            return _id[0].get('id')

class Record(Model):

    """Record model"""

    def add(self, location, comment, _type, user_id=None, status=None, images=None,
                 videos=None, uri=None):
        self.location = location
        self.comment = comment
        assert _type in ['red-flag', 'intervention'], "Wrong incident type.\
                Use 'red-flag' or 'intervention'"
        self.type = _type
        self.createdon = datetime.utcnow()
        self.user_id = user_id or ''
        self.status = status or 'Draft'
        self.images = images or []
        self.videos = videos or []
        self.uri = uri or ''

        query = """insert into records (location, comment, type, createdOn, user_id, status,
        Images, Videos, uri, createdby) values (%(location)s, %(comment)s, %(type)s,
        %(createdon)s, %(user_id)s, %(status)s, %(images)s, %(videos)s,
        %(uri)s, %(createdby)s);"""

        self.query(query,
                   {
                       'location': self.location,
                       'comment': self.comment,
                       'type': self.type,
                       'createdon': self.createdon,
                       'user_id': self.user_id,
                       'status': self.status,
                       'images': self.images,
                       'videos': self.videos,
                       'uri': self.uri,
                       'createdby': self.user_id
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
            
class User(Model):

    """User model"""

    def add(self, username, password, email=None, firstname=None, lastname=None,
                othernames=None, phone_number=None, isadmin=None):

        self.username = username or ''
        self.password = password or ''
        self.email = email or ''
        self.registered = datetime.utcnow()
        self.firstname = firstname or ''
        self.lastname = lastname or ''
        self.othernames = othernames or ''
        self.phone_number = phone_number or ''
        self.isadmin = isadmin or False

        query = """insert into users
        (username, password_hash, email, createdOn, firstname, lastname, othernames,
        phoneNumber, isAdmin)
        values (%(username)s, %(password_hash)s, %(email)s, %(registered)s,
        %(firstname)s, %(lastname)s, %(othernames)s, %(phoneNumber)s, %(isAdmin)s);"""

        self.query(query, {'username': self.username,
                           'password_hash': generate_password_hash(self.password),
                           'email':  self.email,
                           'registered': self.registered,
                           'firstname': self.firstname,
                           'lastname': self.lastname,
                           'othernames': self.othernames,
                           'phoneNumber': self.phone_number,
                           'isAdmin': self.isadmin
                          })

        self.commit()

        

    def all(self):
        """
        Return a list of all users in the database
        """
        query = """select
                id, username, email, firstname, lastname, othernames,
                phoneNumber, isAdmin from users;"""
        self.query(query)

        return self.fetchall()

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
            'isadmin': self.isadmin
            }

    def create_record(self, **kwargs):
        """
        Input - key-value pairs
        """
        user = self.by_username(self.username)
        user_id = user[0]
        record = Record(user_id=user_id, **kwargs)
        record.put()

    def by_username(self, username):
        """
        Returns a user data item with the given username
        as a dictionary.
        """
        query = """ select * from users where username = %s;"""
        self.query(query, (username,))
        record = self.fetchall()
        return record[0] if record else {}

    @staticmethod
    def check_password(password_hash, password):
        """
        Returns True if password hash is valid
        False otherwise.
        """
        return check_password_hash(password_hash, password)

class Blacklist(Model):
    """
    Blacklist Model
    """

    def add(self, jti):
        """
        store token identifier in the database

        :param jti: token identifier
        """
        query = """insert into blacklist (jti) values (%s);"""
        self.query(query, (jti,))
        self.commit()

    
    def is_blacklisted(self, jti):
        """
        Returns True if tokens jti is in the blacklist
        """
        self.query("""select * from blacklist where jti = %s;""",(jti,))
        return bool(self.fetchall())
