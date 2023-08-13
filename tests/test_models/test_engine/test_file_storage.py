#!/usr/bin/python3
"""
Unittest to test FileStorage class
"""
import unittest
import pep8
import json
import os
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.engine.file_storage import FileStorage


class TestFileStorage(unittest.TestCase):
    '''testing file storage'''

    @classmethod
    def setUpClass(cls):
        cls.storage = FileStorage()
        cls.base = BaseModel()
        key = "{}.{}".format(type(cls.base).__name__, cls.base.id)
        cls.rev1 = Review()
        cls.rev1.place_id = "Raleigh"
        cls.rev1.user_id = "Greg"
        cls.rev1.text = "Grade A"

    @classmethod
    def tearDownClass(cls):
        del cls.rev1
        del cls.storage
        del cls.base

    def tearDown(self):
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass

    def test_style_check(self):
        """
        Tests pep8 style
        """
        style = pep8.StyleGuide(quiet=True)
        p = style.check_files(['models/engine/file_storage.py'])
        self.assertEqual(p.total_errors, 0, "fix pep8")

    def test_all(self):
        """
        Tests method: all (returns dictionary <class>.<id> : <obj instance>)
        """
        storage = FileStorage()
        instances_dic = storage.all()
        self.assertIsNotNone(instances_dic)
        self.assertEqual(type(instances_dic), dict)
        self.assertEqual(instances_dic, storage._FileStorage__objects)

    def test_new(self):
        """
        Tests method: new (saves new object into dictionary)
        """
        m_storage = FileStorage()
        instances_dic = m_storage.all()
        melissa = User()
        melissa.first_name = "Melissa"
        m_storage.new(melissa)
        key = melissa.__class__.__name__ + "." + str(melissa.id)
        # print(instances_dic[key])
        self.assertIsNotNone(instances_dic[key])

    def test_save(self):
        """Test save method."""
        self.storage.save()
        with open("file.json", "r", encoding="utf-8") as f:
            save_text = f.read()
            self.assertIn("BaseModel." + self.base.id, save_text)

    def test_reload(self):
        """
        Tests method: reload (reloads objects from string file)
        """
        a_storage = FileStorage()
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass
        with open("file.json", "w") as f:
            f.write("{}")
        with open("file.json", "r") as r:
            for line in r:
                self.assertEqual(line, "{}")
        self.assertIs(a_storage.reload(), None)

    def test_allMethods(self):
        """
        Test method: all methods.
        """
        new_instance = BaseModel()
        fileStore = FileStorage()
        fileStore.new(new_instance)
        fileStore.__objects = {}
        fileStore.reload()
        self.assertEqual(fileStore.all()["BaseModel." + new_instance.id], new_instance)
        