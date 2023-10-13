#!/usr/bin/python3
"""Defines the HBnB console."""
import cmd
import re
from shlex import split
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


def parse(arg):
    curly_braces = re.search(r"\{(.*?)\}", arg)
    brackets = re.search(r"\[(.*?)\]", arg)
    if curly_braces is None:
        if brackets is None:
            return [i.strip(",") for i in split(arg)]
        else:
            lexer = split(arg[:brackets.span()[0]], arg[brackets.span()[1]:])
            retl = [i.strip(",") for i in lexer]
            retl.append(brackets.group())
            return retl
    else:
        lexer = split(arg[:curly_braces.span()[0]], arg[curly_braces.span()[1]:])
        retl = [i.strip(",") for i in lexer]
        retl.append(curly_braces.group())
        return retl


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
            "update": self.do_update,
            "show_id": self.do_show_id,
            "destroy_id": self.do_destroy_id,
            "update_id": self.do_update_id
        }
        match = re.search(r"\.", arg)
        if match is not None:
            arg_list = [arg[:match.span()[0]], arg[match.span()[1]:]]
            match = re.search(r"\((.*?)\)", arg_list[1])
            if match is not None:
                command = [arg_list[1][:match.span()[0]], match.group()[1:-1]]
                if command[0] in arg_dict.keys():
                    call = "{} {}".format(arg_list[0], command[1])
                    return arg_dict[command[0]](call)
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
        arg_list = parse(arg)
        if not arg_list:
            print("** class name missing **")
            return

        class_name = arg_list[0]
        if class_name not in self.class_map:
            print("** class doesn't exist **")
            return

        new_instance = self.class_map[class_name]()
        new_instance.save()
        print(new_instance.id)
        storage.save()

    def do_show(self, arg):
        """Usage: show <class> <id> or <class>.show(<id>)
        Display the string representation of a class instance of a given id.
        """
        arg_list = parse(arg)
        obj_dict = storage.all()
        if not arg_list:
            print("** class name missing **")
            return
        if arg_list[0] not in self.class_map:
            print("** class doesn't exist **")
            return
        if len(arg_list) < 2:
            print("** instance id missing **")
            return

        instance_id = "{}.{}".format(arg_list[0], arg_list[1])
        if instance_id not in obj_dict:
            print("** no instance found **")
            return

        print(obj_dict[instance_id])

    def do_destroy(self, arg):
        """Usage: destroy <class> <id> or <class>.destroy(<id>)
        Delete a class instance of a given id.
        """
        arg_list = parse(arg)
        obj_dict = storage.all()
        if not arg_list:
            print("** class name missing **")
            return
        if arg_list[0] not in self.class_map:
            print("** class doesn't exist **")
            return
        if len(arg_list) < 2:
            print("** instance id missing **")
            return

        instance_id = "{}.{}".format(arg_list[0], arg_list[1])
        if instance_id not in obj_dict:
            print("** no instance found **")
            return

        del obj_dict[instance_id]
        storage.save()

    def do_all(self, arg):
        """Usage: all or all <class> or <class>.all()
        Display string representations of all instances of a given class.
        If no class is specified, displays all instantiated objects.
        """
        arg_list = parse(arg)
        obj_dict = storage.all()
        if arg_list:
            if arg_list[0] not in self.class_map:
                print("** class doesn't exist **")
                return
            obj_list = [str(obj) for obj in obj_dict.values() if isinstance(obj,
                self.class_map[arg_list[0])]
            print(obj_list)
        else:
            obj_list = [str(obj) for obj in obj_dict.values()]
            print(obj_list)

    def do_count(self, arg):
        """Retrieve the number of instances of a class using <class name>.count().

        Usage: <class name>.count()
        """
        arg_list = parse(arg)
        obj_dict = storage.all()

        if arg_list:
            class_name = arg_list[0]
            if class_name in self.class_map:
                count = sum(1 for obj in obj_dict.values() if isinstance(obj,
                    self.class_map[class_name]))
                print(count)
            else:
                print("** class doesn't exist **")
        else:
            print(len(obj_dict))

    def do_update(self, arg):
        """Usage: update <class> <id> <attribute_name> <attribute_value> or
        <class>.update(<id>, <attribute_name>, <attribute_value>) or
        <class>.update(<id>, <dictionary>)
        Update a class instance of a given id by adding or updating 
        a given attribute key/value pair or dictionary.
        """
        arg_list = parse(arg)
        obj_dict = storage.all()

        if not arg_list:
            print("** class name missing **")
            return
        if arg_list[0] not in self.class_map:
            print("** class doesn't exist **")
            return
        if len(arg_list) < 2:
            print("** instance id missing **")
            return
        instance_id = "{}.{}".format(arg_list[0], arg_list[1])
        if instance_id not in obj_dict:
            print("** no instance found **")
            return
        if len(arg_list) < 3:
            print("** attribute name missing **")
            return
        if len(arg_list) < 4:
            print("** value missing **")
            return
        obj = obj_dict[instance_id]
        attribute_name = arg_list[2]
        attribute_value = arg_list[3]

        if attribute_name in obj.__class__.__dict__:
            value_type = type(obj.__class__.__dict__[attribute_name])
            obj.__dict__[attribute_name] = value_type(attribute_value)
        else:
            obj.__dict__[attribute_name] = attribute_value
        storage.save()

    def do_show_id(self, arg):
        """Retrieve an instance based on its ID using <class name>.show(<id>).

        Usage: <class name>.show(<id>)
        """
        match = re.search(r"^(.+)\.show\((.+)\)$", arg)
        if match:
            class_name = match.group(1)
            instance_id = match.group(2)
            obj_dict = storage.all()
            if class_name not in self.class_map:
                print("** class doesn't exist **")
                return
            instance_key = "{}.{}".format(class_name, instance_id)
            if instance_key in obj_dict:
                print(obj_dict[instance_key])
            else:
                print("** no instance found **")
        else:
            print("*** Unknown syntax: {}".format(arg))

    def do_destroy_id(self, arg):
        """Destroy an instance based on its ID using <class name>.destroy(<id>).

        Usage: <class name>.destroy(<id>)
        """
        match = re.search(r"^(.+)\.destroy\((.+)\)$", arg)
        if match:
            class_name = match.group(1)
            instance_id = match.group(2)
            obj_dict = storage.all()
            if class_name not in self.class_map:
                print("** class doesn't exist **")
                return
            instance_key = "{}.{}".format(class_name, instance_id)
            if instance_key in obj_dict:
                del obj_dict[instance_key]
                storage.save()
            else:
                print("** no instance found **")
        else:
            print("*** Unknown syntax: {}".format(arg))

    def do_update_id(self, arg):
        """Update an instance based on its ID using <class name>.update
        (<id>, <attribute name>, <attribute value>).

        Usage: <class name>.update(<id>, <attribute name>, <attribute value>)
        """
        match = re.search(r"^(.+)\.update\((.+), (.+), (.+)\)$", arg)
        if match:
            class_name = match.group(1)
            instance_id = match.group(2)
            attribute_name = match.group(3)
            attribute_value = match.group(4)
            obj_dict = storage.all()
            if class_name not in self.class_map:
                print("** class doesn't exist **")
                return
            instance_key = "{}.{}".format(class_name, instance_id)
            if instance_key in obj_dict:
                obj = obj_dict[instance_key]
                if hasattr(obj, attribute_name):
                    attr_type = type(getattr(obj, attribute_name))
                    setattr(obj, attribute_name, attr_type(attribute_value))
                    obj.save()
                else:
                    setattr(obj, attribute_name, attribute_value)
                    obj.save()
            else:
                print("** no instance found **")
        else:
            print("*** Unknown syntax: {}".format(arg))


if __name__ == "__main__":
    HBNBCommand().cmdloop()
