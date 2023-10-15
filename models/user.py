#!/usr/bin/python3
"""Defines the User class."""
from models.base_model import BaseModel

class User(BaseModel):
    """Represents a User.

    Attributes:
        email (str): The email of the user.
        password (str): The password of the user.
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.
    """

    email = ""
    password = ""
    first_name = ""
    last_name = ""

    @classmethod
    def all(cls):
        """Retrieve all instances of the User class."""
        from models import storage
        return storage.all(User)

    @classmethod
    def count(cls):
        """Count the number of instances of the User class."""
        from models import storage
        return len(storage.all(User))
