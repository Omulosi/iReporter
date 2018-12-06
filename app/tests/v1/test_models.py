"""
    app.tests.v1.models
    ~~~~~~~~~~~~~~~~~~~

    Tests for the database's Record model

"""

import unittest
from app.api.v1.models import Record, User, connect, create_record_table, create_user_table, Model
from instance.config import TestConfig
from collections import OrderedDict



class RecordModel(unittest.TestCase):

    def setUp(self):

        # create tables in test_db database
        #create_user_table(TestConfig)
        #create_record_table(TestConfig)
        # Create record objects but dont store them in the database
        create_record_table(TestConfig)
        create_user_table(TestConfig)

        self.r_data = {'location': "-1, 36", 'comment': "Judges soliciting for bribes"}
        self.r1 = Record(**self.r_data)
        self.r2 = Record(**self.r_data)
        self.u_data = {'username': "paul", 'email': "paul@mail"}
        self.u1 = User(**self.u_data)
        self.u1.set_password('secret')
        self.u2 = User(**self.u_data)
        self.u2.set_password('secret')

    def tearDown(self):
        Record.clear_all()

    def test_get_all(self):
        self.assertEqual(Record.all(), [])
        Record.put(self.r1)
        Record.put(self.r2)
        self.assertEqual(len(Record.all()), 2)

        Record.clear_all()
        User.clear_all()


    def test_get_by_id(self):
        r = Record(**self.r_data)
        Record.put(r)
        User.put(self.u1)
        self.assertEqual(type(r.serialize), OrderedDict)
        self.assertEqual(Record.by_id(27777474), []) # non-existent id
        self.assertEqual(User.by_id(27777474), []) # non-existent id

        Record.clear_all()
        User.clear_all()


    def test_put_record(self):
        Record.clear_all()
        User.clear_all()
        # checks that db storage fails if item is not of type Model
        with self.assertRaises(AssertionError):
                Record.put({'id': 2})
        with self.assertRaises(AssertionError):
                User.put([{'id': 5}])

        # Confrim the item is stored

        self.assertEqual(Record.put(self.r1), None)
        self.assertEqual(User.put(self.u1), None)
        self.assertEqual(Record.by_id(1), [])
        self.assertEqual(User.by_id(1), [])

        Record.clear_all()
        User.clear_all()


    def test_delete(self):

        Record.put(self.r1)
        self.assertEqual(Record.delete(1), None)
        self.assertEqual(Record.by_id(1), []) # Record deleted


        Record.clear_all()
        User.clear_all()

    def test_serialize(self):

        self.assertIsInstance(self.r1.serialize, OrderedDict)
        Record.clear_all()
        User.clear_all()


    def test_clear_all(self):

        Record.put(self.r1)
        Record.put(self.r2)
        self.assertEqual(Record.clear_all(), None)
        self.assertEqual(Record.all(), [])
        Record.clear_all()
        User.clear_all()

    def test_required_field_present_at_initialization(self):
        self.assertEqual(self.r1.video, [])
        self.assertEqual(self.r1.image, [])
        self.assertEqual(self.r1.type, 'red-flag')
        self.assertEqual(self.r1.location, "-1, 36")
        self.assertEqual(self.r1.comment, "Judges soliciting for bribes")
        self.assertEqual(self.r1.status, "Under Investigation")

if __name__ == '__main__':
    unittest.main(verbosity=2)
