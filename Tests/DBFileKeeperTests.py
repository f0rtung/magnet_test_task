import os
import unittest

from WSGI.DBFileKeeper import DBFileKeeper


class DBFileKeeperTests(unittest.TestCase):
    def setUp(self):
        self.db_file_name = "testDB.sqlite"
        self.db_file = DBFileKeeper(self.db_file_name)

    def test_is_db_file_exist(self):
        self.assertFalse(self.db_file.is_exist())

    def test_create_db_file(self):
        self.assertTrue(self.db_file.create_db_file())
        self.assertTrue(self.db_file.delete_db_file())

    def test_db_file_path(self):
        db_path = os.path.join("DataBase", self.db_file_name)
        self.assertEqual(self.db_file.get_path(), db_path)

if __name__ == '__main__':
    unittest.main()
