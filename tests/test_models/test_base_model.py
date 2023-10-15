#!/usr/bin/python3
"""Defines unittests for models/base_model.py.

Unittest classes:
    TestBaseModelInstantiation
    TestBaseModelSave
    TestBaseModelToDict
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.base_model import BaseModel

class TestBaseModelInstantiation(unittest.TestCase):
    """Unittests for testing instantiation of the BaseModel class."""

    def test_no_args_instantiates(self):
        self.assertIsInstance(BaseModel(), BaseModel)

    def test_new_instance_stored_in_objects(self):
        self.assertIn(BaseModel(), models.storage.all().values())

    def test_id_is_public_str(self):
        self.assertIsInstance(BaseModel().id, str)

    def test_created_at_is_public_datetime(self):
        self.assertIsInstance(BaseModel().created_at, datetime)

    def test_updated_at_is_public_datetime(self):
        self.assertIsInstance(BaseModel().updated_at, datetime)

    def test_two_models_unique_ids(self):
        model1 = BaseModel()
        model2 = BaseModel()
        self.assertNotEqual(model1.id, model2.id)

    def test_two_models_different_created_at(self):
        model1 = BaseModel()
        sleep(0.001)  # Sleep for a short duration to ensure a time difference
        model2 = BaseModel()
        self.assertNotEqual(model1.created_at, model2.created_at)

    def test_two_models_different_updated_at(self):
        model1 = BaseModel()
        sleep(0.001)  # Sleep for a short duration to ensure a time difference
        model2 = BaseModel()
        self.assertNotEqual(model1.updated_at, model2.updated_at)

    def test_str_representation(self):
        model = BaseModel()
        model.id = "123456"
        str_repr = str(model)
        self.assertTrue(str_repr.startswith("[BaseModel]"))
        self.assertIn(model.id, str_repr)

    def test_args_unused(self):
        model = BaseModel(42)
        self.assertNotEqual(model, 42)

    def test_instantiation_with_kwargs(self):
        data = {
            'id': '123',
            'created_at': '2023-10-11T12:00:00.000000',
            'name': 'TestModel'
        }
        model = BaseModel(**data)
        self.assertEqual(model.id, data['id'])
        self.assertEqual(model.created_at, datetime.strptime(data['created_at'], "%Y-%m-%dT%H:%M:%S.%f"))
        self.assertEqual(model.name, data['name'])

    def test_instantiation_with_None_kwargs(self):
        model = BaseModel(**{})
        self.assertIsInstance(model, BaseModel)

    def test_instantiation_with_args_and_kwargs(self):
        data = {
            'id': '123',
            'created_at': '2023-10-11T12:00:00.000000',
            'name': 'TestModel'
        }
        model = BaseModel(42, **data)
        self.assertEqual(model.id, data['id'])
        self.assertEqual(model.created_at, datetime.strptime(data['created_at'], "%Y-%m-%dT%H:%M:%S.%f"))
        self.assertEqual(model.name, data['name'])


class TestBaseModelSave(unittest.TestCase):
    """Unittests for testing save method of the BaseModel class."""

    @classmethod
    def setUpClass(cls):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    @classmethod
    def tearDownClass(cls):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_one_save(self):
        model = BaseModel()
        initial_updated_at = model.updated_at
        model.save()
        self.assertNotEqual(initial_updated_at, model.updated_at)

    def test_two_saves(self):
        model = BaseModel()
        initial_updated_at = model.updated_at
        model.save()
        updated_updated_at = model.updated_at
        self.assertNotEqual(initial_updated_at, updated_updated_at)
        model.save()
        self.assertNotEqual(updated_updated_at, model.updated_at)

    def test_save_with_arg(self):
        model = BaseModel()
        with self.assertRaises(TypeError):
            model.save(42)

    def test_save_updates_file(self):
        model = BaseModel()
        model.save()
        with open("file.json", "r") as f:
            self.assertTrue(len(f.read()) > 0)

class TestBaseModelToDict(unittest.TestCase):
    """Unittests for testing to_dict method of the BaseModel class."""

    def test_to_dict_type(self):
        model = BaseModel()
        model_dict = model.to_dict()
        self.assertIsInstance(model_dict, dict)

    def test_to_dict_contains_correct_keys(self):
        model = BaseModel()
        model_dict = model.to_dict()
        expected_keys = ["id", "created_at", "updated_at", "__class__"]
        for key in expected_keys:
            self.assertIn(key, model_dict)

    def test_to_dict_contains_added_attributes(self):
        model = BaseModel()
        model.name = "TestModel"
        model.number = 42
        model_dict = model.to_dict()
        self.assertIn("name", model_dict)
        self.assertIn("number", model_dict)

    def test_to_dict_datetime_attributes_are_strs(self):
        model = BaseModel()
        model_dict = model.to_dict()
        self.assertIsInstance(model_dict["created_at"], str)
        self.assertIsInstance(model_dict["updated_at"], str)

    def test_to_dict_output(self):
        model = BaseModel()
        model_dict = model.to_dict()
        self.assertEqual(model_dict["id"], model.id)
        self.assertEqual(model_dict["created_at"], model.created_at.isoformat())
        self.assertEqual(model_dict["updated_at"], model.updated_at.isoformat())
        self.assertEqual(model_dict["__class__"], "BaseModel")

    def test_contrast_to_dict_dunder_dict(self):
        model = BaseModel()
        model_dict = model.to_dict()
        self.assertNotEqual(model_dict, model.__dict__)

    def test_to_dict_with_arg(self):
        model = BaseModel()
        with self.assertRaises(TypeError):
            model.to_dict(None)

if __name__ == "__main__":
    unittest.main()
