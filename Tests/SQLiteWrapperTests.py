import unittest
import os
from WSGI.WSGIApplication import WSGIApplication


class SQLiteWrapperTests(unittest.TestCase):
    def setUp(self):
        os.remove(os.path.join("DataBase", "base.sqlite"))
        self.sqlite_DB = WSGIApplication.get_or_create_db_object("../create_db.sql")

    def test_check_init_db_data(self):
        all_regions = self.sqlite_DB.get_all_regions()
        all_cities = self.sqlite_DB.get_all_cities()
        self.assertEqual(3, len(all_regions))
        self.assertEqual(9, len(all_cities))

    def test_try_insert_different_regions(self):
        def check_insert(region_name, assert_func):
            insert_result = self.sqlite_DB.insert_query(
                "INSERT INTO Regions (RegionName) VALUES(?)",
                (region_name,)
            )
            assert_func(insert_result)

        check_insert("Краснодарский край", self.assertIsNone)
        check_insert("Ростовская область", self.assertIsNone)
        check_insert("Ставропольский край", self.assertIsNone)
        check_insert("Республика коми", self.assertIsNotNone)

    def test_try_insert_different_cities(self):
        def check_insert(city_name, assert_func):
            insert_result = self.sqlite_DB.insert_query(
                "INSERT INTO Cities (CityName) VALUES(?)",
                (city_name,)
            )
            assert_func(insert_result)

        check_insert("Краснодар", self.assertIsNone)
        check_insert("Ростов", self.assertIsNone)
        check_insert("Сыктывкар", self.assertIsNotNone)


if __name__ == '__main__':
    unittest.main()
