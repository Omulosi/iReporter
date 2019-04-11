'''
    app.tests.v2.test_db
    --------------------

    Tests for database initialization functions
'''

import pytest
import psycopg2
from app.db.db import get_db


def test_get_close_db(app):
    with app.app_context():
        db = get_db()
        assert db is get_db()

    with pytest.raises(psycopg2.InterfaceError) as e:
        db.cursor().execute('SELECT 1')

    assert 'closed' in str(e)

def test_init_db_command(runner, monkeypatch):
    class Recorder(object):
        called = False

    def fake_init_db():
        Recorder.called = True

    monkeypatch.setattr('app.db.init_db', fake_init_db)
    result = runner.invoke(args=['init-db'])
    assert 'Initialized' in result.output
    assert Recorder.called

def test_clear_all_db_command(runner, monkeypatch):
    class Recorder(object):
        called = False

    def fake_clear_tables():
        Recorder.called = True

    monkeypatch.setattr('app.db.clear_tables', fake_clear_tables)
    result = runner.invoke(args=['clear-all-db'])
    assert 'cleared' in result.output
    assert Recorder.called

def test_rollback_db_command(runner, monkeypatch):
    class Recorder(object):
        called = False

    def fake_rollback():
        Recorder.called = True

    monkeypatch.setattr('app.db.rollback', fake_rollback)
    result = runner.invoke(args=['rollback-db'])
    assert 'rolled back' in result.output
    assert Recorder.called