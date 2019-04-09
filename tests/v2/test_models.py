"""
    app.tests.v2.auth
    ~~~~~~~~~~~~~~~~~~~
"""

from app.api.v2.models import Record, User, Blacklist
from datetime import datetime
import pytest
import json
from app.api.utils import make_token_header


def test_create_record(client):
    user = User(username='john', password='iamsosecret')
    user.put()
    user_id = User.get_last_inserted_id()
    record1 = Record(location='23,34', comment='conmen', _type='intervention', user_id=user_id)
    record2 = Record(location='23,34', comment='conmen', _type='intervention', user_id=user_id)
    record1.put()
    record2.put()
    r1_id = Record.get_last_inserted_id()
    r2_id = Record.get_last_inserted_id()
    all_records = Record.all()
    assert len(all_records) == 2

def test_delete_record(client):
    user = User(username='john', password='iamsosecret')
    user.put()
    user_id = User.get_last_inserted_id()
    record = Record(location='23,34', comment='conmen', _type='intervention', user_id=user_id)
    record.put()
    r_id = Record.get_last_inserted_id()
    Record.delete(r_id)
    assert not bool(Record.by_id(r_id))

def test_update_record(client):
    user = User(username='john', password='iamsosecret')
    user.put()
    user_id = User.get_last_inserted_id()
    record = Record(location='23,34', comment='conmen', _type='intervention', user_id=user_id)
    record.put()
    r_id = Record.get_last_inserted_id()
    Record.update(r_id, 'comment', 'principled')
    data = Record.by_id(r_id)
    assert data[0]['comment'] == 'principled'

def test_get_all_records(client):
        user = User(username='john', password='iamsosecret')
        user.put()
        user_id = User.get_last_inserted_id()
        record1 = Record(location='23,34', comment='conmen', _type='intervention', user_id=user_id)
        record2 = Record(location='23,34', comment='conmen', _type='intervention', user_id=user_id)
        record3 = Record(location='23,34', comment='conmen', _type='intervention', user_id=user_id)
        record1.put()
        record2.put()
        record3.put()
        all_records = Record.all()
        assert len(all_records) == 3

def test_create_user(client):
    user = User(username='john', password='iamsosecret')
    user.put()
    user_id = User.get_last_inserted_id()
    assert bool(user_id)
    assert type(user.serialize) == dict
    u = User.by_id(user_id)[0]
    pass_hash = u.get('password_hash')
    assert User.check_password(pass_hash, 'iamsosecret')

def test_delete_user(client):
    user = User(username='john', password='iamsosecret')
    user.put()
    user_id = User.get_last_inserted_id()
    User.delete(user_id)
    user = User.by_id(user_id)
    assert not bool(user)
