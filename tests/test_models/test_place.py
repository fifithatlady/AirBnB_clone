#!/usr/bin/python3
"""Unit tests for models/place.py."""

import unittest
from models.place import Place
import models
import os
from datetime import datetime


class TestPlace(unittest.TestCase):
    """Test the Place class."""

    def setUp(self):
        self.place = Place()

    def test_instance(self):
        """Test that place is an instance of Place."""
        self.assertIsInstance(self.place, Place)

    def test_id_is_string(self):
        """Test that the id of place is a string."""
        self.assertIsInstance(self.place.id, str)

    def test_city_id_is_string(self):
        """Test that city_id of place is a string."""
        self.assertIsInstance(self.place.city_id, str)

    def test_user_id_is_string(self):
        """Test that user_id of place is a string."""
        self.assertIsInstance(self.place.user_id, str)

    def test_name_is_string(self):
        """Test that name of place is a string."""
        self.assertIsInstance(self.place.name, str)

    def test_description_is_string(self):
        """Test that description of place is a string."""
        self.assertIsInstance(self.place.description, str)

    def test_number_rooms_is_int(self):
        """Test that number_rooms of place is an integer."""
        self.assertIsInstance(self.place.number_rooms, int)

    def test_number_bathrooms_is_int(self):
        """Test that number_bathrooms of place is an integer."""
        self.assertIsInstance(self.place.number_bathrooms, int)

    def test_max_guest_is_int(self):
        """Test that max_guest of place is an integer."""
        self.assertIsInstance(self.place.max_guest, int)

    def test_price_by_night_is_int(self):
        """Test that price_by_night of place is an integer."""
        self.assertIsInstance(self.place.price_by_night, int)

    def test_latitude_is_float(self):
        """Test that latitude of place is a float."""
        self.assertIsInstance(self.place.latitude, float)

    def test_longitude_is_float(self):
        """Test that longitude of place is a float."""
        self.assertIsInstance(self.place.longitude, float)

    def test_amenity_ids_is_list(self):
        """Test that amenity_ids of place is a list."""
        self.assertIsInstance(self.place.amenity_ids, list)

    def test_created_at_is_datetime(self):
        """Test that created_at of place is a datetime object."""
        self.assertIsInstance(self.place.created_at, datetime)

    def test_updated_at_is_datetime(self):
        """Test that updated_at of place is a datetime object."""
        self.assertIsInstance(self.place.updated_at, datetime)

    def test_save(self):
        """Test that save method updates the updated_at attribute."""
        original_updated_at = self.place.updated_at
        self.place.save()
        self.assertNotEqual(original_updated_at, self.place.updated_at)

    def test_to_dict(self):
        """Test that to_dict method returns a dictionary."""
        place_dict = self.place.to_dict()
        self.assertIsInstance(place_dict, dict)

    def test_to_dict_includes_class(self):
        """Test that the to_dict method includes the class name."""
        place_dict = self.place.to_dict()
        self.assertEqual(place_dict['__class__'], 'Place')

    def test_to_dict_includes_id(self):
        """Test that the to_dict method includes the 'id' attribute."""
        place_dict = self.place.to_dict()
        self.assertIn('id', place_dict)

    def test_to_dict_includes_created_at(self):
        """Test that the to_dict method includes the 'created_at' attribute."""
        place_dict = self.place.to_dict()
        self.assertIn('created_at', place_dict)

    def test_to_dict_includes_updated_at(self):
        """Test that the to_dict method includes the 'updated_at' attribute."""
        place_dict = self.place.to_dict()
        self.assertIn('updated_at', place_dict)

    def test_str(self):
        """Test that the str method has the correct output."""
        place_str = str(self.place)
        self.assertIn("[Place]", place_str)
        self.assertIn(str(self.place.id), place_str)

    def test_args_unused(self):
        """Test that passing args to Place is not allowed."""
        pl = Place(None)
        self.assertNotIn(None, pl.__dict__.values())

    def test_instantiation_with_kwargs(self):
        """Test that Place can be instantiated with kwargs."""
        dt = datetime.today()
        dt_iso = dt.isoformat()
        place = Place(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(place.id, "345")
        self.assertEqual(place.created_at, dt)
        self.assertEqual(place.updated_at, dt)

    def test_instantiation_with_None_kwargs(self):
        """Test that Place can't be instantiated with None kwargs."""
        with self.assertRaises(TypeError):
            Place(id=None, created_at=None, updated_at=None)


if __name__ == '__main__':
    unittest.main()

