#!/usr/bin/python3
"""
Module - file_storage

Serializes instances to a JSON file
and deserializes JSON file to instances
"""
import json
from models.base_model import BaseModel
from models.user import User
from models.city import City
from models.place import Place
from models.state import State
from models.review import Review
from models.amenity import Amenity


class FileStorage:
    """
    Serializes instances to a JSON file
    and deserializes JSON file to instances
    """
    __file_path = "file.json"
    __objects = {}
    __class_dict = {
                    "BaseModel": BaseModel,
                    "User": User,
                    "Place": Place,
                    "City": City,
                    "State": State,
                    "Review": Review,
                    "Amenity": Amenity
                 }

    def all(self):
        """
        Returns the dictionary __objects
        """
        return self.__objects

    def new(self, obj):
        """
        Sets in __objects the obj with key
        <obj class name>.id
        """
        self.__objects[f"{obj.__class__.__name__}.{obj.id}"] = obj

    def save(self):
        """
        Serializes __objects to the JSON file
        '__file_path'
        """
        save_data = {}
        for key, val in self.__objects.items():
            if isinstance(val, dict):
                save_data[key] = val
            else:
                save_data[key] = val.to_dict()
        with open(self.__file_path, "w", encoding='utf8') as file:
            json.dump(save_data, file, indent=2)

    def reload(self):
        """
        Deserializes the JSON file to __objects
        (only if the JSON file '__file_path' exists;
        otherwise, do nothing. If the file doesn't exist,
        no exception should be raised)
        """
        try:
            with open(self.__file_path, "r", encoding='utf8') as file:
                reload_data = json.load(file)
            for key, obj in reload_data.items():
                self.__objects.update({key: (self.__class_dict
                                      [obj["__class__"]](**obj))})
        except FileNotFoundError:
            pass
