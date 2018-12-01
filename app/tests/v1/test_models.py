"""
    app.tests.v1.models
    ~~~~~~~~~~~~~~~~~~~

    Tests for the database model
"""

import unittest
from app.api.v1.models import Record

class RecordModel(unittest.TestCase):

    def setUp(self):
        # Create record objects but dont store them in the database
        self.r1 = Record(location="-1, 36", comment="Judges soliciting for bribes")
        self.r2 = Record(location="18, 55", comment="Judges soliciting for bribes")

    def tearDown(self):
        Record.clear_all()

    def test_get_all(self):
        # Database initially empty
        self.assertEqual(Record.all(), [])
        Record.put(self.r1)
        Record.put(self.r2)
        self.assertEqual(len(Record.all()), 2)

    def test_get_by_id(self):
        r = Record(location="-1, 36", comment="Judges soliciting for bribes")
        Record.put(r)
        r_id = r.data_id
        id_2 = 'id_two'

        self.assertEqual(Record.by_id(r_id), r)
        self.assertEqual(Record.by_id(id_2), None)
        self.assertEqual(Record.by_id(27777474), None) # non-existent id

    def test_put_record(self):
        self.assertEqual(Record.put(self.r1), True)
        # checks that db storage fails if item is not of type Model
        with self.assertRaises(ValueError):
                Record.put({'id': 2})
        with self.assertRaises(ValueError):
                Record.put([{'id': 5}])

    def test_delete(self):
        r = Record(location="-1, 36", comment="Judges soliciting for bribes")
        Record.put(r)
        r_id = r.data_id
        self.assertEqual(Record.delete(r_id), True)
        self.assertEqual(Record.delete(4444), None)
        self.assertEqual(Record.delete('key'), None)

    def test_serialize(self):
        r = Record(location="-1, 36", comment="Judges soliciting for bribes")
        self.assertEqual(type(r.serialize), dict)

    def test_add_field(self):
        r = Record(location="-1, 36", comment="Judges soliciting for bribes")
        r.add_field('name','test')
        self.assertEqual(r.name, 'test')

if __name__ == '__main__':
    unittest.main(verbosity=2)
