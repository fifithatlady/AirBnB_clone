#!/usr/bin/python3
"""Unittests for models/city.py."""

import unittest
from datetime import datetime
from time import sleep
from models.city import City

class TestCity(unittest.TestCase):
    def test_city_instantiation(self):
        city = City()
        self.assertIsInstance(city, City)

    def test_city_id(self):
        city = City()
        self.assertIsInstance(city.id, str)

    def test_city_created_at(self):
        city = City()
        self.assertIsInstance(city.created_at, datetime)

    def test_city_updated_at(self):
        city = City()
        self.assertIsInstance(city.updated_at, datetime)

    def test_city_state_id_attribute(self):
        city = City()
        self.assertTrue(hasattr(city, 'state_id'))
        self.assertIsInstance(city.state_id, str)

    def test_city_name_attribute(self):
        city = City()
        self.assertTrue(hasattr(city, 'name'))
        self.assertIsInstance(city.name, str)

    def test_city_unique_ids(self):
        city1 = City()
        city2 = City()
        self.assertNotEqual(city1.id, city2.id)

    def test_city_created_at_change(self):
        city1 = City()
        sleep(0.05)
        city2 = City()
        self.assertLess(city1.created_at, city2.created_at)

    def test_city_updated_at_change(self):
        city1 = City()
        sleep(0.05)
        city2 = City()
        self.assertLess(city1.updated_at, city2.updated_at)

    def test_city_to_dict(self):
        city = City(
            state_id='state_id_value',
            id='id_value',
            name='name_value'
        )

        city_dict = city.to_dict()

        self.assertIsInstance(city_dict, dict)
        self.assertIn('id', city_dict)
        self.assertIn('state_id', city_dict)
        self.assertIn('name', city_dict)
        self.assertIn('__class__', city_dict)
        self.assertEqual(city_dict['__class__'], 'City')

    def test_city_str_representation(self):
        city = City()
        city.id = "123456"
        dt = datetime.today()
        city.created_at = dt
        city.updated_at = dt
        str_repr = str(city)
        self.assertIn("[City] (123456)", str_repr)
        self.assertIn("'id': '123456'", str_repr)
        self.assertIn("'created_at': {}".format(repr(dt)), str_repr)
        self.assertIn("'updated_at': {}".format(repr(dt)), str_repr)

    def test_city_save(self):
        city = City()
        original_updated_at = city.updated_at
        city.save()
        self.assertNotEqual(original_updated_at, city.updated_at)

if __name__ == "__main__":
    unittest.main()
