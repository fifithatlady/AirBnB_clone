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
        """Usage: <class name>.show(<id>)
        Display the string representation of a class instance of a given id.
        """
        parts = arg.split(".")
        class_name = parts[0]
        if class_name in self.class_map:
            if len(parts) == 2:
                instance_id = parts[1]
                instance = self.class_map[class_name].show(instance_id)
                if instance:
                    print(instance)
                else:
                    print("** no instance found **")
            else:
                print("** instance id missing **")
        else:
            print("** class doesn't exist **")

    def do_destroy(self, arg):
        """Usage: <class name>.destroy(<id>)
        Delete a class instance of a given id.
        """
        parts = arg.split(".")
        class_name = parts[0]
        if class_name in self.class_map:
            if len(parts) == 2:
                instance_id = parts[1]
                result = self.class_map[class_name].destroy(instance_id)
                if result:
                    storage.save()
                else:
                    print("** no instance found **")
            else:
                print("** instance id missing **")
        else:
            print("** class doesn't exist **")

    def do_all(self, arg):
        """Usage: <class name>.all()
        Display string representations of all instances of a given class.
        If no class is specified, displays all instantiated objects.
        """
        parts = arg.split(".")
        if parts[0] in self.class_map:
            class_name = parts[0]
            instances = self.class_map[class_name].all()
            obj_list = [str(instance) for instance in instances]
            print(obj_list)
        else:
            obj_dict = storage.all()
            if parts[0]:
                print("** class doesn't exist **")
            else:
                obj_list = [str(obj) for obj in obj_dict.values()]
                print(obj_list)

    def do_count(self, arg):
        """Usage: <class name>.count()
        Retrieve the number of instances of a given class.
        """
        parts = arg.split(".")
        class_name = parts[0]
        if class_name in self.class_map:
            count = self.class_map[class_name].count()
            print(count)
        else:
            print("** class doesn't exist **")

    def do_update(self, arg):
        """Usage: <class name>.update(<id>, <attribute name>, <attribute value>)
        Update a class instance of a given id by adding or updating
        a given attribute key/value pair.
        """
        args = arg.split()
        if len(args) < 3:
            print("** class name missing **" if len(args) < 1 else
                  "** instance id missing **" if len(args) < 2 else
                  "** attribute name missing **")
            return

        class_name, instance_id, attribute_name = args[0], args[1], args[2]
        if class_name in self.class_map:
            if len(args) < 4:
                print("** value missing **")
            else:
                attribute_value = args[3]
                self.class_map[class_name].update(instance_id, attribute_name, attribute_value)
                storage.save()
        else:
            print("** class doesn't exist **")

    def do_update(self, arg):
        """Usage: <class name>.update(<id>, <dictionary representation>)
        Update a class instance of a given id with a dictionary representation.
        """
        parts = arg.split(".")
        if len(parts) == 2 and parts[0] in self.class_map:
            class_name, instance_id = parts[0], parts[1]
            instance_key = f"{class_name}.{instance_id}"
            obj_dict = storage.all()
            if instance_key in obj_dict:
                instance = obj_dict[instance_key]
                if not isinstance(instance, BaseModel):
                    return
                if len(parts) == 2:
                    try:
                        instance_dict = eval(input("Enter a dictionary: "))
                        if isinstance(instance_dict, dict):
                            instance.update(instance_dict)
                            storage.save()
                    except:
                        pass

if __name__ == "__main__":
    HBNBCommand().cmdloop()
