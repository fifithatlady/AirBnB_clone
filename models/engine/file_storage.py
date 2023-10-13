#!/usr/bin/python3
"""Defines the FileStorage class."""

import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review

class FileStorage:
    """Represents an abstracted storage engine."""

    def __init__(self, file_path="file.json"):
        self.__file_path = file_path
        self.__objects = {}

    def all(self) -> dict:
        """Return the dictionary of objects."""
        return self.__objects

    def new(self, obj) -> None:
        """Set an object in the objects dictionary."""
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        self.__objects[key] = obj

    def save(self) -> None:
        """Serialize objects to the JSON file."""
        obj_dict = {key: obj.to_dict() for key, obj in self.__objects.items()}
        with open(self.__file_path, "w") as file:
            json.dump(obj_dict, file)

    def reload(self) -> None:
        """Deserialize the JSON file to objects, if it exists."""
        try:
            with open(self.__file_path, "r") as file:
                obj_dict = json.load(file)
                for key, obj_data in obj_dict.items():
                    class_name = obj_data.get("__class__")
                    if class_name:
                        del obj_data["__class__"]
                        obj_instance = eval(class_name)(**obj_data)
                        self.new(obj_instance)
        except FileNotFoundError:
            pass

