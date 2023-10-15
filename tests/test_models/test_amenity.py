#!/usr/bin/python3
"""Unittests for models/amenity.py."""
import unittest
import os
from datetime import datetime
from time import sleep
from models.amenity import Amenity
import models

class TestAmenity(unittest.TestCase):
    def test_amenity_instantiation(self):
        amenity = Amenity()
        self.assertIsInstance(amenity, Amenity)

    def test_amenity_id(self):
        amenity = Amenity()
        self.assertIsInstance(amenity.id, str)

    def test_amenity_created_at(self):
        amenity = Amenity()
        self.assertIsInstance(amenity.created_at, datetime)

    def test_amenity_updated_at(self):
        amenity = Amenity()
        self.assertIsInstance(amenity.updated_at, datetime)

    def test_amenity_name_attribute(self):
        amenity = Amenity()
        self.assertTrue(hasattr(amenity, 'name'))
        self.assertIsInstance(amenity.name, str)
        self.assertEqual(amenity.name, "")

    def test_amenity_unique_ids(self):
        amenity1 = Amenity()
        amenity2 = Amenity()
        self.assertNotEqual(amenity1.id, amenity2.id)

    def test_amenity_created_at_change(self):
        amenity1 = Amenity()
        sleep(0.05)
        amenity2 = Amenity()
        self.assertLess(amenity1.created_at, amenity2.created_at)

    def test_amenity_updated_at_change(self):
        amenity1 = Amenity()
        sleep(0.05)
        amenity2 = Amenity()
        self.assertLess(amenity1.updated_at, amenity2.updated_at)

    def test_amenity_to_dict(self):
        amenity = Amenity()
        amenity_dict = amenity.to_dict()
        self.assertIsInstance(amenity_dict, dict)
        self.assertIn('id', amenity_dict)
        self.assertIn('created_at', amenity_dict)
        self.assertIn('updated_at', amenity_dict)
        self.assertIn('__class__', amenity_dict)
        self.assertEqual(amenity_dict['__class__'], 'Amenity')

    def test_amenity_str_representation(self):
        amenity = Amenity()
        amenity.id = "123456"
        dt = datetime.today()
        amenity.created_at = dt
        amenity.updated_at = dt
        str_repr = str(amenity)
        self.assertIn("[Amenity] (123456)", str_repr)
        self.assertIn("'id': '123456'", str_repr)
        self.assertIn("'created_at': {}".format(repr(dt)), str_repr)
        self.assertIn("'updated_at': {}".format(repr(dt)), str_repr)

    def test_amenity_save(self):
        amenity = Amenity()
        original_updated_at = amenity.updated_at
        amenity.save()
        self.assertNotEqual(original_updated_at, amenity.updated_at)

    def test_amenity_save_file_update(self):
        amenity = Amenity()
        amenity.save()
        amenity_id = "Amenity." + amenity.id
        with open("file.json", "r") as file:
            self.assertIn(amenity_id, file.read())

if __name__ == "__main__":
    unittest.main()
