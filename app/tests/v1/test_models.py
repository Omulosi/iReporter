"""
    app.tests.v1.models
    ~~~~~~~~~~~~~~~~~~~

    Tests for the database's Record model

"""

import unittest
from app.api.v1.ireporter_db import Record
from app.api.v1.config_db import create_tables, connect
from instance.config import TestDBConfig

class IncidentModel(unittest.TestCase):

    def setUp(self):
        # Create Incident objects but dont store them in the database
        db = connect(TestDBConfig)
        cursor = db.cursor()
        cursor.execute('drop table if exists records')
        create_tables(TestDBConfig)
        self.data = {'location': "-1, 36", 'comment': "Judges soliciting for bribes"}
        self.r1 = Record(**self.data)
        self.r2 = Record(**self.data)
        Record.put(self.r1)
        Record.put(self.r2)

    def tearDown(self):
        Record.clear_all()

    def test_get_all(self):

        self.assertEqual(len(Record.all()), 2)

    def test_get_by_id(self):
        # r = Record(**self.data)
        # Record.put(r)
        # r_id = r.data_id
        # id_2 = 'id_two'

        self.assertEqual(len(Record.all()), 2)

        self.assertEqual(Record.by_id(1), [])
        self.assertIsNotNone(Record.by_id(2))
        self.assertEqual(Record.by_id(27777474), None) # non-existent id

    def test_put_record(self):
        self.assertEqual(Record.put(self.r1), True)
        # checks that db storage fails if item is not of type Model
        with self.assertRaises(ValueError):
                Record.put({'id': 2})
        with self.assertRaises(ValueError):
                Record.put([{'id': 5}])

    def test_delete(self):
        r = Record(**self.data)
        Record.put(r)
        r_id = r.data_id
        self.assertEqual(Record.delete(r_id), True)
        self.assertEqual(Record.delete(4444), None)
        self.assertEqual(Record.delete('key'), None)

    def test_serialize(self):
        r = Record(**self.data)
        self.assertEqual(type(r.serialize), dict)
        self.assertEqual(len(r.serialize), 10)

    def test_add_field(self):
        r = Record(**self.data)
        r.add_field('name','test')
        self.assertEqual(r.name, 'test')

    def test_clear_all(self):
        r = Record(**self.data)
        Record.put(r)
        self.assertEqual(Record.clear_all(), None)
        self.assertEqual(Record.all(), [])

    def test_all_field_present_at_initialization(self):
        self.assertEqual(self.r2.data_id, self.r1.data_id + 1)
        self.assertEqual(self.r1.video, [])
        self.assertEqual(self.r1.image, [])
        self.assertEqual(self.r1.type, 'red-flag')
        self.assertEqual(self.r1.location, "-1, 36")
        self.assertEqual(self.r1.comment, "Judges soliciting for bribes")
        self.assertEqual(self.r1.status, "Under Investigation")
        self.assertEqual(self.r1.user, None)

if __name__ == '__main__':
    unittest.main(verbosity=2)
