#!/usr/bin/python3
"""Unittests for models/state.py."""

import unittest
from datetime import datetime
from models.state import State
from models.base_model import BaseModel

class TestState(unittest.TestCase):
    def test_instantiation_with_kwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        state = State(id="345", created_at=dt_iso,
                updated_at=dt_iso, name="California")
        self.assertEqual(state.id, "345")
        self.assertEqual(state.created_at, dt)
        self.assertEqual(state.updated_at, dt)
        self.assertEqual(state.name, "California")

    def test_instantiation(self):
        state = State()
        self.assertIsInstance(state, BaseModel)
        self.assertIsInstance(state.created_at, datetime)
        self.assertIsInstance(state.updated_at, datetime)
        self.assertEqual(state.name, "")

    def test_name_type(self):
        state = State()
        self.assertIsInstance(state.name, str)

    def test_to_dict(self):
        state = State()
        state.id = "123"
        state.name = "Sample State Name"
        d = state.to_dict()
        self.assertEqual(d["id"], "123")
        self.assertEqual(d["name"], "Sample State Name")
        self.assertEqual(d["__class__"], "State")

    def test_save(self):
        state = State()
        original_updated_at = state.updated_at
        state.save()
        self.assertNotEqual(original_updated_at, state.updated_at)

    def test_two_states_unique_ids(self):
        state1 = State()
        state2 = State()
        self.assertNotEqual(state1.id, state2.id)

    def test_two_states_different_created_at(self):
        state1 = State()
        state2 = State()
        self.assertLess(state1.created_at, state2.created_at)

    def test_two_states_different_updated_at(self):
        state1 = State()
        state2 = State()
        self.assertLess(state1.updated_at, state2.updated_at)

if __name__ == "__main__":
    unittest.main()
