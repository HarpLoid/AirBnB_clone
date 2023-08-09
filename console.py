#!/usr/bin/python3
"""
Module - console

Entry point of the
command interpreter
"""
import cmd
from models import storage
from models.base_model import BaseModel
from models.user import User


class HBNBCommand(cmd.Cmd):
    """
    command interpreter class
    """
    prompt     = "(hbnb) "
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
                    "User": User
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
        args = line.split()
        if len(args) >= 4:
            key = f"{args[0]}.{args[1]}"
            cast = type(args[3])
            attrib_value = cast(args[3])
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

    def help_quit(self):
        """
        Help for quit
        """
        print('\n'.join(['(hbnb) quit',
                         'Exits program with "quit"']))

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
            completions = [ i for i in iterable
                            if i.startswith(text)]
        return completions




if __name__ == "__main__":
    HBNBCommand().cmdloop()
