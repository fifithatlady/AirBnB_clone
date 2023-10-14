#!/usr/bin/python3
"""Defines the HBnB console."""
import cmd
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """Defines the HolbertonBnB command interpreter.

    Attributes:
        prompt (str): The command prompt.
    """
    prompt = "(hbnb) "
    class_map = {
        "BaseModel": BaseModel,
        "User": User,
        "State": State,
        "City": City,
        "Place": Place,
        "Amenity": Amenity,
        "Review": Review
    }

    def emptyline(self):
        """Do nothing upon receiving an empty line."""
        pass

    def default(self, arg):
        """Default behavior for cmd module when input is invalid"""
        arg_dict = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update
        }
        split_args = arg.split(".")
        if len(split_args) == 2 and split_args[0] in self.class_map:
            class_name = split_args[0]
            cmd = split_args[1]
            if cmd in arg_dict:
                return arg_dict[cmd](f"{class_name} {split_args[1]}")

        print("*** Unknown syntax: {}".format(arg))
        return False

    def do_quit(self, arg):
        """Quit command to exit the program."""
        return True

    def do_EOF(self, arg):
        """EOF signal to exit the program."""
        print("")
        return True

    def do_create(self, arg):
        """Usage: create <class>
        Create a new class instance and print its id.
        """
        class_name = arg.strip()
        if not class_name:
            print("** class name missing **")
            return

        if class_name in self.class_map:
            new_instance = self.class_map[class_name]()
            new_instance.save()
            print(new_instance.id)
            storage.save()
        else:
            print("** class doesn't exist **")

    def do_show(self, arg):
        """Usage: show <class> <id> or <class>.show(<id>)
        Display the string representation of a class instance of a given id.
        """
        args = arg.split()
        obj_dict = storage.all()
        if len(args) < 2:
            print("** class name missing **" if len(args) < 1 else "** instance id missing **")
            return

        class_name, instance_id = args[0], args[1]

        if class_name in self.class_map:
            instance = obj_dict.get(f"{class_name}.{instance_id}")
            if instance:
                print(instance)
            else:
                print("** no instance found **")
        else:
            print("** class doesn't exist **")

    def do_destroy(self, arg):
        """Usage: destroy <class> <id> or <class>.destroy(<id>)
        Delete a class instance of a given id.
        """
        args = arg.split()
        obj_dict = storage.all()
        if len(args) < 2:
            print("** class name missing **" if len(args) < 1 else "** instance id missing **")
            return

        class_name, instance_id = args[0], args[1]

        if class_name in this.class_map:
            instance_key = f"{class_name}.{instance_id}"
            if instance_key in obj_dict:
                del obj_dict[instance_key]
                storage.save()
            else:
                print("** no instance found **")
        else:
            print("** class doesn't exist **")

    def do_all(self, arg):
        """Usage: all or all <class> or <class>.all()
        Display string representations of all instances of a given class.
        If no class is specified, displays all instantiated objects.
        """
        args = arg.split()
        obj_dict = storage.all()

        if len(args) == 0:
            print([str(obj) for obj in obj_dict.values()])
        elif len(args) == 1:
            class_name = args[0]
            if class_name in self.class_map:
                instances = storage.all(self.class_map[class_name])
                print([str(obj) for obj in instances])
            else:
                print("** class doesn't exist **")

    def do_count(self, arg):
        """Usage: count <class> or <class>.count()
        Retrieve the number of instances of a given class.
        """
        args = arg.split()
        obj_dict = storage.all()

        if len(args) == 0:
            print(len(obj_dict))
        elif len(args) == 1:
            class_name = args[0]
            if class_name in self.class_map:
                count = sum(1 for obj in obj_dict.values() if isinstance(obj, self.class_map[class_name]))
                print(count)
            else:
                print("** class doesn't exist **")

    def do_update(self, arg):
        """Usage: update <class> <id> <attribute_name> <attribute_value> or
       <class>.update(<id>, <attribute_name>, <attribute_value>) or
       <class>.update(<id>, <dictionary>)
        Update a class instance of a given id by adding or updating
        a given attribute key/value pair or dictionary.
        """
        args = arg.split()
        obj_dict = storage.all()

        if len(args) < 3:
            print("** class name missing **" if len(args) < 1 else
                  "** instance id missing **" if len(args) < 2 else
                  "** attribute name missing **")
            return

        class_name, instance_id, attribute_name = args[0], args[1], args[2]
        instance_key = f"{class_name}.{instance_id}"

        if class_name in self.class_map:
            if instance_key in obj_dict:
                instance = obj_dict[instance_key]

                if len(args) == 3:
                    print("** value missing **")
                    return

                if len(args) == 4:
                    attribute_value = args[3]
                else:
                    attribute_value = args[4]

                setattr(instance, attribute_name, attribute_value)
                instance.save()
            else:
                print("** no instance found **")
        else:
            print("** class doesn't exist **")


if __name__ == "__main__":
    HBNBCommand().cmdloop()
