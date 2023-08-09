#!/usr/bin/python3
"""
Module - user

User Class
"""
from models.base_model import BaseModel


class User(BaseModel):
    """
    class User that inherits from BaseModel
    """
    email = ""
    password = ""
    first_name = ""
    last_name = ""
