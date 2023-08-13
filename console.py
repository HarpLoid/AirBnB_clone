#!/usr/bin/python3
"""
Module - console

Entry point of the
command interpreter
"""
import re
import cmd
import json
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
    __class_dict = {
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
        elif line not in self.__class_dict:
            print(self.error_msg["2"])
        else:
            instance = self.__class_dict[line]()
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
        elif args[0] not in self.__class_dict:
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
        elif args[0] not in self.__class_dict:
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
        if line in self.__class_dict:
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
        object_list = []
        if len(line) == 0:
            for obj in storage.all().values():
                object_list.append(str(obj))
            print(object_list)
        elif line in self.__class_dict:
            for key, obj in storage.all().items():
                if line in key:
                    object_list.append(str(obj))
            print(object_list)
        else:
            print(self.error_msg["2"])

    def do_update(self, line):
        """
         Updates an instance based on the class name and id
         by adding or updating attribute and saves
         the changes into the JSON file.
        """
        print("line",line)
        args = []
        pattern = r'(.*)(\{[^\}]*\})'
        match = re.match(pattern, line)
        if match:
            args = match.group(1).split()
            class_name = args[0]
            class_id = args[1].strip('"')
            key = f"{class_name}.{class_id}"
            try:
                dict_arg = json.loads(match.group(2))
                args.append(dict_arg)
            except json.decoder.JSONDecodeError:
                args.append("")
        else:
            args = shlex.split(line)
            class_name = args[0]
            class_id = args[1].strip('"')
            key = f"{class_name}.{class_id}"

        if len(args) >= 4:
            if class_name in self.__class_dict:
                if hasattr(self.__class_dict[class_name], args[2]):
                    cast = type(getattr(self.__class_dict[class_name], args[2]))
                    attrib_value = cast(args[3])
                    try:
                        setattr(storage.all()[key], args[2], attrib_value)
                        storage.all()[key].save()
                    except KeyError:
                        print(self.error_msg["4"])
                else:
                    try:
                        setattr(storage.all()[key], args[2], args[3])
                        storage.all()[key].save()
                    except KeyError:
                        print(self.error_msg["4"])
            else:
                print(self.error_msg["2"])

        elif len(args) == 0:
            print(self.error_msg["1"])
        elif args[0] not in self.__class_dict:
            print(self.error_msg["2"])
        elif len(args) == 1:
            print(self.error_msg["3"])
        elif f"{class_name}.{class_id}" not in storage.all():
            print(self.error_msg["4"])
        elif len(args) == 2:
            print(self.error_msg["5"])
        else:
            if isinstance(args[2], dict):
                add_dict = args[2]
                for k, v in add_dict.items():
                    if hasattr(self.__class_dict[class_name], k):
                        cast = type(getattr(self.__class_dict[class_name], k))
                        attrib_value = cast(v)
                        try:
                            setattr(storage.all()[key], k, attrib_value)
                            storage.all()[key].save()
                        except KeyError:
                            print(self.error_msg["4"])
                    else:
                        try:
                            setattr(storage.all()[key], k, v)
                            storage.all()[key].save()
                        except KeyError:
                            print(self.error_msg["4"])
            else:
                print(self.error_msg["6"])

    def default(self, line):
        args = self.parse(line)
        if len(args) == 0:
            print(f"*** Unknown syntax {line}")
        try:
            if args['command'] == 'all':
                HBNBCommand.do_all(self, args['class_name'])
            elif args['command'] == 'count':
                HBNBCommand.do_count(self, args['class_name'])
            elif args['command'] == 'show':
                arg = f"{args['class_name']} {args['id_val']}"
                HBNBCommand.do_show(self, arg)
            elif args['command'] == 'destroy':
                arg = f"{args['class_name']} {args['id_val']}"
                HBNBCommand.do_destroy(self, arg)
            elif args['command'] == 'update':
                if args['dict_rep']:
                    arg = "{} {} {}".format(args['class_name'],
                                            args['id_val'],
                                            args['dict_rep'])
                else:
                    arg = "{} {} {} {}".format(args['class_name'],
                                               args['id_val'],
                                               args['attrib_name'],
                                               args['attrib_val'])
                HBNBCommand.do_update(self, arg)
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
        print('\n'.join(['(hbnb) <class name>.destroy(<id>)',
                         'Deletes an instance based on the class name and id',
                         'then saves the changes into the JSON file']))

    def help_all(self):
        print('\n'.join(['(hbnb) <class name>.all() or (hbnb) all',
                         'Prints all string representation',
                         'of all instances based or not on the class name.']))

    def help_create(self):
        print('\n'.join(['(hbnb) create <class name>',
                         'Creates a new instance of <class name>',
                         'saves it and  prints the id']))

    def help_show(self):
        print('\n'.join(['(hbnb) <class name>.show(<id>)',
                         'Prints the string representation',
                         'of an instance based on class name and id']))

    def help_update(self):
        print('\n'.join(['(hbnb) <class name>.update(<id>\
                         <attribute name> <attribute value>)',
                         'Updates an instance based on the class name and id',
                         'by adding or updating attribute and saves',
                         'the changes into the JSON file.']))

    def complete_update(self, text, line, begidx, endidx):
        """
        completes args for update command
        """
        return self.completion(self.__class_dict.keys(), text)

    def complete_show(self, text, line, begidx, endidx):
        """
        completes args for show command
        """
        return self.completion(self.__class_dict.keys(), text)

    def complete_destroy(self, text, line, begidx, endidx):
        """
        completes args for destroy command
        """
        return self.completion(self.__class_dict.keys(), text)

    def complete_create(self, text, line, begidx, endidx):
        """
        completes args for create command
        """
        return self.completion(self.__class_dict.keys(), text)

    def complete_all(self, text, line, begidx, endidx):
        """
        completes args for all command
        """
        return self.completion(self.__class_dict.keys(), text)

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
        pattern = r'''(\w+)\.([^(]+)\((\s*|[^,]+)(?:,\s*({.*?}))?
                    (?:,\s*([^,]+))?(?:,\s*([^)]+))?\)'''
        # pattern = r'''(\w+)\.(\w+)\(([^,]+)?(?:,\s*({.*?}))?
        #            (?:,\s*(\w+),\s*["\']([^"\']+)["\'])?\)'''
        match = re.match(pattern, line, re.VERBOSE)

        if match:
            args_dict['class_name'] = match.group(1)
            args_dict['command'] = match.group(2)
            if match.group(3) is not None:
                args_dict['id_val'] = match.group(3)
            else:
                args_dict['id_val'] = ""
            if match.group(4) is not None:
                args_dict['dict_rep'] = match.group(4)
            else:
                args_dict['dict_rep'] = ""
            if match.group(5) is not None:
                args_dict['attrib_name'] = match.group(5)
            else:
                args_dict['attrib_name'] = ""
            if match.group(6) is not None:
                args_dict['attrib_val'] = match.group(6)
            else:
                args_dict['attrib_val'] = ""

            return args_dict
        else:
            return args_dict


if __name__ == "__main__":
    HBNBCommand().cmdloop()
