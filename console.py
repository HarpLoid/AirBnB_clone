#!/usr/bin/python3
"""
Module - console

Entry point of the
command interpreter
"""
import cmd
from models import storage
from models.base_model import BaseModel


class HBNBCommand(cmd.Cmd):
    """
    command interpreter class
    """
    prompt     = "(hbnb) "
    class_dict = {
                   "BaseModel": BaseModel
                 }
    error_msg  = {
                   "1": '** class name missing **',
                   "2": '** class doesn\'t exist **',
                   "3": '** instance id missing **',
                   "4": '** no instance found **'
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

    def help_quit(self):
        """
        Help for quit
        """
        print('\n'.join(['(hbnb) quit',
                         'Exits program with "quit"']))

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
        print(f"'{line}'", type(line))
        if len(line) == 0:
            print(self.error_msg["1"])
        elif line not in self.class_dict:
            print(self.error_msg["2"])
        else:
            instance = self.class_dict[line]()
            instance.save()
            print(instance.id)

    def help_create(self):
        print('\n'.join(['(hbnb) create <class name>',
                         'Creates a new instance of <class name>',
                         'saves it and  prints the id']))

    def complete_create(self, text, line, begidx, endidx):
        """
        completes args for create command
        """
        return self.completion(self, text)
        #if not text:
        #    completions = list(self.class_dict.keys())
        #else:
        #    completions = [ i for i in self.class_dict.keys()
        #                    if i.startswith(text)]
        #return completions

    def do_show(self, line):
        """
        (hbnb) show <class name> <id>

        Prints the string representation
        of an instance based on the class name and id.
        """
        args = line.split()
        try:
            key = f"{args[0]}.{args[1]}"
        except IndexError:
            pass
        print(args)
        if len(args) == 0:
            print(self.error_msg["1"])
        elif args[0] not in self.class_dict:
            print(self.error_msg["2"])
        elif len(args) == 1:
            print(self.error_msg["3"])
        elif key not in storage.all():
            print(self.error_msg["4"])
        else:
            print(storage.all()[key])

    def help_show(self):
        print('\n'.join(['(hbnb) show <class name> <id>',
                         'Prints the string representation',
                         'of an instance based on class name and id']))

    @staticmethod
    def completion(self, text):
        """
        completes args for create command
        """
        if not text:
            completions = list(self.class_dict.keys())
        else:
            completions = [ i for i in self.class_dict.keys()
                            if i.startswith(text)]
        return completions




if __name__ == "__main__":
    HBNBCommand().cmdloop()
