"""
    app.tests.v2.auth
    ~~~~~~~~~~~~~~~~~~~
"""

from app.models import Record, User, Blacklist
from datetime import datetime
import pytest
import json
from app.helpers import make_token_header


def test_create_record(client):
    RECORD = Record()
    USER = User()
    USER.add(username='john', password='iamsosecret')
    user_id = USER.get_last_inserted_id()
    RECORD.add(location='23,34', comment='conmen', _type='intervention', user_id=user_id)
    RECORD.add(location='23,34', comment='conmen', _type='intervention', user_id=user_id)
    all_records = RECORD.all()
    assert len(all_records) == 2

def test_delete_record(client):
    RECORD = Record()
    USER = User()
    USER.add(username='john', password='iamsosecret')
    user_id = USER.get_last_inserted_id()
    RECORD.add(location='23,34', comment='conmen', _type='intervention', user_id=user_id)
    r_id = RECORD.get_last_inserted_id()
    RECORD.delete(r_id)
    assert not bool(RECORD.by_id(r_id))

def test_update_record(client):
    RECORD = Record()
    USER = User()
    USER.add(username='john', password='iamsosecret')
    user_id = USER.get_last_inserted_id()
    RECORD.add(location='23,34', comment='conmen', _type='intervention', user_id=user_id)
    r_id = RECORD.get_last_inserted_id()
    RECORD.update(r_id, 'comment', 'principled')
    data = RECORD.by_id(r_id)
    assert data[0]['comment'] == 'principled'

def test_get_all_records(client):
    RECORD = Record()
    USER = User()
    USER.add(username='john', password='iamsosecret')
    user_id = USER.get_last_inserted_id()
    RECORD.add(location='23,34', comment='conmen', _type='intervention', user_id=user_id)
    RECORD.add(location='23,34', comment='conmen', _type='intervention', user_id=user_id)
    RECORD.add(location='23,34', comment='conmen', _type='intervention', user_id=user_id)
    all_records = RECORD.all()
    assert len(all_records) == 3

def test_create_user(client):
    RECORD = Record()
    USER = User()
    USER.add(username='john', password='iamsosecret')
    user_id = USER.get_last_inserted_id()
    assert bool(user_id)
    u = USER.by_id(user_id)[0]
    pass_hash = u.get('password_hash')
    assert USER.check_password(pass_hash, 'iamsosecret')

def test_delete_user(client):
    RECORD = Record()
    USER = User()
    USER.add(username='john', password='iamsosecret')
    user_id = USER.get_last_inserted_id()
    USER.delete(user_id)
    user = USER.by_id(user_id)
    assert not bool(user)
