from datetime import datetime
from nose.tools import raises
from io import StringIO
import unittest
from .. import DummyDB, DummyDBException


class TestDummyDB(unittest.TestCase):

    def test_dummydb_basic(self):
        """
        Test if we can create a db object.
        """
        db = DummyDB()

    def test_dummydb_new_table(self):
        """
        Test if we can create a new table for a new db.
        """
        db = DummyDB()
        columns = {
            "one": int,
            "two": str,
            "three": bool,
        }
        db.create_table("new_table", columns)

    @raises(DummyDBException)
    def test_dummydb_new_table_duplicate_name(self):
        """
        Ensure we raise an exception when we try to create a table again.
        """
        db = DummyDB()
        columns = {
            "one": int,
            "two": str,
            "three": bool,
        }
        db.create_table("new_table", columns)
        db.create_table("new_table", columns)

    @raises(DummyDBException)
    def test_dummydb_add_data_to_nonexistant_table(self):
        """
        """
        db = DummyDB()
        db.insert("nonexistant_table", one=1, two="haunted", three=True)

    @raises(DummyDBException)
    def test_dummydb_add_data_to_table_wrong_column_name(self):
        """
        Try to add some data and read it back
        """
        db = DummyDB()
        columns = {
            "one": int,
            "two": str,
            "three": bool,
        }
        db.create_table("new_table", columns)
        result = db.select("new_table", four=1)

    @raises(DummyDBException)
    def test_dummydb_add_data_to_table_wrong_column_type(self):
        """
        Try to add some data and read it back
        """
        db = DummyDB()
        columns = {
            "one": int,
            "two": str,
            "three": bool,
        }
        db.create_table("new_table", columns)
        result = db.select("new_table", two=1)

    def test_dummydb_add_data_to_table(self):
        """
        Try to add some data and read it back
        """
        db = DummyDB()
        columns = {
            "one": int,
            "two": str,
            "three": bool,
        }
        db.create_table("new_table", columns)
        db.insert("new_table", one=1, two="haunted", three=True)
        result = db.select("new_table", one=1)
        self.assertEqual(result[0]['two'], "haunted")

    def test_dummydb_datetime_column(self):
        """
        Make sure we handle datetime data correctly.
        """
        db = DummyDB()
        columns = {
            "one": int,
            "two": str,
            "three": bool,
            "four": datetime,
        }
        db.create_table("new_table", columns)
        db.insert("new_table", one=1, two="haunted", three=True, four=datetime(year=2020, month=3, day=13))
        result = db.select("new_table", one=1)
        self.assertEqual(result[0]['three'], True)

        filehandle = StringIO()
        db.write_to_filehandle(filehandle)
        db.load_from_filehandle(filehandle)

        result = db.select("new_table", one=1)
        self.assertEqual(result[0]['three'], True)
