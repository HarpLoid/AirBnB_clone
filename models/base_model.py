#!/usr/bin/python3
"""
Module - base_model

BaseModel defines all the common
attributes/methods for other classes
"""
from uuid import uuid4
from datetime import datetime
import models


class BaseModel:
    """
    Base class that defines all
    common attributes and methods
    for other classe
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes the object
        """
        if kwargs is not None and len(kwargs) > 0:
            date_format = "%Y-%m-%dT%H:%M:%S.%f"
            for k, v in kwargs.items():
                if k == "__class__":
                    pass
                elif k == "created_at":
                    self.created_at = datetime.strptime(v, date_format)
                elif k == "updated_at":
                    self.updated_at = datetime.strptime(v, date_format)
                else:
                    setattr(self, k, v)
        else:
            self.id = str(uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            models.storage.new(self)

    def __str__(self):
        """
        returns the string representation
        of the class
        """
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    def save(self):
        """
        updates the public instance attribute
        updated_at with the current datetime
        """
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """
        returns a dictionary containing all
        keys/values of __dict__ of the instance
        """
        data_dict = self.__dict__.copy()
        update_dict = {
                        "__class__":str(self.__class__.__name__),
                        "created_at":self.created_at.isoformat(),
                        "updated_at":self.updated_at.isoformat()
                      }
        data_dict.update(update_dict)
        return data_dict
