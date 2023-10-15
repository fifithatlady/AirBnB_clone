#!/usr/bin/python3
"""Defines the HBnB console."""
import cmd
from models import storage
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.review import Review
from models.amenity import Amenity
from models.base_model import BaseModel

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
        "Review": Review,
        "Amenity": Amenity
    }

    def emptyline(self):
        """Do nothing upon receiving an empty line."""
        pass

    def default(self, arg):
        """Default behavior for cmd module when input is invalid"""
        split_args = arg.split(".")
        if len(split_args) == 2:
            class_name = split_args[0]
            cmd = split_args[1]

            if class_name in self.class_map:
                if cmd == "all()":
                    self.do_all(class_name)
                elif cmd == "count()":
                    self.do_count(class_name)
                elif cmd.startswith("show(") and cmd.endswith(")"):
                    instance_id = cmd.split("(")[1].split(")")[0]
                    self.do_show(f"{class_name} {instance_id}")
                elif cmd.startswith("destroy(") and cmd.endswith(")"):
                    instance_id = cmd.split("(")[1].split(")")[0]
                    self.do_destroy(f"{class_name} {instance_id}")
                elif cmd.startswith("update(") and cmd.endswith(")"):
                    update_args = cmd.split("(")[1].split(")")[0].split(",")
                    if len(update_args) >= 2:
                        instance_id = update_args[0].strip()
                        attribute_name = update_args[1].strip()
                        if len(update_args) >= 3:
                            attribute_value = update_args[2].strip()
                            self.do_update(f"{class_name} {instance_id} {attribute_name} {attribute_value}")
                        else:
                            self.do_update(f"{class_name} {instance_id} {attribute_name}")
                    else:
                        print("*** Unknown syntax: {}".format(arg))
                else:
                    print("*** Unknown syntax: {}".format(arg))
            else:
                print("*** Unknown syntax: {}".format(arg))
        else:
            print("*** Unknown syntax: {}".format(arg))

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
            instance_key = f"{class_name}.{instance_id}"
            instance = obj_dict.get(instance_key)
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
            obj_list = [str(obj) for obj in obj_dict.values()]
            print(obj_list)
        elif len(args) == 1:
            class_name = args[0]
            if class_name in this.class_map:
                obj_list = [str(obj) for obj in obj_dict.values()
                        if isinstance(obj, this.class_map[class_name])]
                print(obj_list)
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
            if class_name in this.class_map:
                count = sum(1 for obj in obj_dict.values()
                        if isinstance(obj, this.class_map[class_name]))
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

        if class_name in this.class_map:
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

