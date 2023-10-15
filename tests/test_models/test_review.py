#!/usr/bin/python3
"""Unittests for models/review.py"""

import unittest
from models.review import Review
from datetime import datetime

class TestReview(unittest.TestCase):
    """Test the Review class."""

    def test_instantiation(self):
        review = Review()
        self.assertIsInstance(review, Review)
        self.assertIsInstance(review.created_at, datetime)
        self.assertIsInstance(review.updated_at, datetime)
        self.assertEqual(review.place_id, "")
        self.assertEqual(review.user_id, "")
        self.assertEqual(review.text, "")

    def test_to_dict(self):
        review = Review()
        review.id = "123"
        d = review.to_dict()
        self.assertEqual(d["id"], "123")
        self.assertEqual(d["__class__"], "Review")

    def test_save(self):
        review = Review()
        original_updated_at = review.updated_at
        review.save()
        self.assertNotEqual(original_updated_at, review.updated_at)

    def test_types(self):
        review = Review()
        self.assertIsInstance(review.place_id, str)
        self.assertIsInstance(review.user_id, str)
        self.assertIsInstance(review.text, str)

    def test_empty_string_place_id(self):
        review = Review(place_id="")
        self.assertEqual(review.place_id, "")

    def test_empty_string_user_id(self):
        review = Review(user_id="")
        self.assertEqual(review.user_id, "")

    def test_empty_string_text(self):
        review = Review(text="")
        self.assertEqual(review.text, "")

    def test_none_place_id(self):
        review = Review(place_id=None)
        self.assertIsNone(review.place_id)

    def test_none_user_id(self):
        review = Review(user_id=None)
        self.assertIsNone(review.user_id)

    def test_none_text(self):
        review = Review(text=None)
        self.assertIsNone(review.text)

    def test_long_text(self):
        text = "A" * 5000
        review = Review(text=text)
        self.assertEqual(review.text, text)

    def test_special_characters_text(self):
        text = "Special characters: $%^"
        review = Review(text=text)
        self.assertEqual(review.text, text)

if __name__ == "__main__":
    unittest.main()

