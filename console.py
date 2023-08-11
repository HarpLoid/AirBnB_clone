#!/usr/bin/python3
"""
Module - console

Entry point of the
command interpreter
"""
import re
import cmd
import shlex
from models import storage
from models.user import User
from models.city import City
from models.place import Place
from models.state import State
from models.review import Review
from models.amenity import Amenity
from models.base_model import BaseModel


class HBNBCommand(cmd.Cmd):
    """
    command interpreter class
    """
    prompt = "(hbnb) "
    error_msg = {
        "1": '** class name missing **',
        "2": '** class doesn\'t exist **',
        "3": '** instance id missing **',
        "4": '** no instance found **',
        "5": '** attribute name missing **',
        "6": '** value missing **'
    }
    class_dict = {
        "BaseModel": BaseModel,
        "User": User,
        "Place": Place,
        "City": City,
        "State": State,
        "Review": Review,
        "Amenity": Amenity
    }

    def do_EOF(self, line):
        """
        (hbnb) ctrl + D
        Exits program using ctrl + D
        """
        return True

    def do_quit(self, line):
        """
        (hbnb) quit
        Exits program with command "quit"
        """
        return True

    def emptyline(self):
        """
        Does nothing when no command
        is executed
        """

    def do_create(self, line):
        """
        (hbnb) create <class name>

        Creates new instance of class,
        saves it and prints the id
        """
        if len(line) == 0:
            print(self.error_msg["1"])
        elif line not in self.class_dict:
            print(self.error_msg["2"])
        else:
            instance = self.class_dict[line]()
            instance.save()
            print(instance.id)

    def do_show(self, line):
        """
        (hbnb) show <class name> <id>

        Prints the string representation
        of an instance based on the class name and id.
        """
        args = line.split()
        if len(args) == 0:
            print(self.error_msg["1"])
        elif args[0] not in self.class_dict:
            print(self.error_msg["2"])
        elif len(args) == 1:
            print(self.error_msg["3"])
        elif (f"{args[0]}.{args[1]}") not in storage.all():
            print(self.error_msg["4"])
        else:
            key = f"{args[0]}.{args[1]}"
            print(storage.all()[key])

    def do_destroy(self, line):
        """
        Deletes an instance based on the class name and id
        (save the change into the JSON file).
        """
        args = line.split()
        if len(args) == 0:
            print(self.error_msg["1"])
        elif args[0] not in self.class_dict:
            print(self.error_msg["2"])
        elif len(args) == 1:
            print(self.error_msg["3"])
        elif (f"{args[0]}.{args[1]}") not in storage.all():
            print(self.error_msg["4"])
        else:
            key = f"{args[0]}.{args[1]}"
            del storage.all()[key]
            storage.save()

    def do_count(self, line):
        """
        <class name>.count()
        Returns the number of instances of a class.
        """
        if line in self.class_dict:
            count = 0

            for key in storage.all():
                if line in key:
                    count += 1
            print(count)
        else:
            print(self.error_msg["1"])

    def do_all(self, line):
        """
        Prints all string representation
        of all instances based or not on the class name. 
        """
        if len(line) == 0:
            for obj in storage.all().values():
                print(str(obj))
        elif line in self.class_dict:
            for key, obj in storage.all().items():
                if line in key:
                    print(str(obj))
        else:
            print(self.error_msg["2"])

    def do_update(self, line):
        """
         Updates an instance based on the class name and id
         by adding or updating attribute and saves
         the changes into the JSON file.
        """
        args = shlex.split(line)
        if len(args) >= 4:
            key = f"{args[0]}.{args[1]}"
            if hasattr(self.class_dict[args[0]], args[2]):
                cast = type(getattr(self.class_dict[args[0]], args[2]))
                print(cast)
                attrib_value = cast(args[3])
            else:
                attrib_value = args[3]
            setattr(storage.all()[key], args[2], attrib_value)
            storage.all()[key].save()
        elif len(args) == 0:
            print(self.error_msg["1"])
        elif args[0] not in self.class_dict:
            print(self.error_msg["2"])
        elif len(args) == 1:
            print(self.error_msg["3"])
        elif (f"{args[0]}.{args[1]}") not in storage.all():
            print(self.error_msg["4"])
        elif len(args) == 2:
            print(self.error_msg["5"])
        else:
            print(self.error_msg["6"])

    def default(self, line):
        args = self.parse(line)
        if len(args) == 1:
            print(f"*** Unknown syntax {line}")
            return
        try:
            if args['command'] == 'all':
                HBNBCommand.do_all(self, args['class_name'])
            elif args['command'] == 'count':
                HBNBCommand.do_count(self, args['class_name'])
            elif args['command'] == 'show':
                arg = args['class_name'] + ' ' + args['id_val']
                HBNBCommand.do_count(self, arg)
            elif args['command'] == 'destroy':
                arg = args['class_name'] + ' ' + args['id_val']
                HBNBCommand.do_count(self, arg)
            elif args['command'] == 'update':
                arg = args['class_name'] + ' ' + args['id_value'] + ' '\
                    + args['attrib_name'] + ' ' + args['attrib_val']
                HBNBCommand.do_count(self, arg)
            else:
                print(f"*** Unknown syntax {line}")
        except IndexError:
            print(f"*** Unknown syntax {line}")

    def help_quit(self):
        """
        Help for quit
        """
        print('\n'.join(['(hbnb) quit',
                         'Exits program with "quit"']))

    def help_count(self):
        print('\n'.join(['(hbnb) <class name>.count()',
                         'Returns the number of instances of a class.']))

    def help_destroy(self):
        print('\n'.join(['(hbnb) destroy <class name> <id>',
                         'Deletes an instance based on the class name and id',
                         'then saves the changes into the JSON file']))

    def help_all(self):
        print('\n'.join(['(hbnb) all <class name> or (hbnb) all',
                         'Prints all string representation',
                         'of all instances based or not on the class name.']))

    def help_create(self):
        print('\n'.join(['(hbnb) create <class name>',
                         'Creates a new instance of <class name>',
                         'saves it and  prints the id']))

    def help_show(self):
        print('\n'.join(['(hbnb) show <class name> <id>',
                         'Prints the string representation',
                         'of an instance based on class name and id']))

    def help_update(self):
        print('\n'.join(['(hbnb) update <class name> <id> <attribute name> "<attribute value>"',
                         'Updates an instance based on the class name and id',
                         'by adding or updating attribute and saves',
                         'the changes into the JSON file.']))

    def complete_update(self, text, line, begidx, endidx):
        """
        completes args for update command
        """
        return self.completion(self.class_dict.keys(), text)

    def complete_show(self, text, line, begidx, endidx):
        """
        completes args for show command
        """
        return self.completion(self.class_dict.keys(), text)

    def complete_destroy(self, text, line, begidx, endidx):
        """
        completes args for destroy command
        """
        return self.completion(self.class_dict.keys(), text)

    def complete_create(self, text, line, begidx, endidx):
        """
        completes args for create command
        """
        return self.completion(self.class_dict.keys(), text)

    def complete_all(self, text, line, begidx, endidx):
        """
        completes args for all command
        """
        return self.completion(self.class_dict.keys(), text)

    @staticmethod
    def completion(iterable, text):
        """
        completes args function
        """
        if not text:
            completions = list(iterable)
        else:
            completions = [i for i in iterable
                           if i.startswith(text)]
        return completions

    @staticmethod
    def parse(line):
        args_dict = {}
        pattern = r'^(.*?)\.([^(]+)\(([^)]+)(?:,\s*({.*?}))?\
                    (?:,\s*([^,]+),\s*([^)]+))?\)$'
        match = re.match(pattern, line)

        if match:
            args_dict['class_name'] = match.group(1)
            args_dict['command'] = match.group(2)
            args_dict['id_val'] = match.group(3)
            args_dict['dict_rep'] = match.group(4)
            args_dict['attrib_name'] = match.group(5)
            args_dict['attrib_val'] = match.group(6)

        return args_dict


if __name__ == "__main__":
    HBNBCommand().cmdloop()
