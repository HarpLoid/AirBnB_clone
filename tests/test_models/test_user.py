#!/usr/bin/python3
"""
Unittest for User class
"""
import unittest
import os
import pep8
from models.user import User
from models.base_model import BaseModel


class TestUser(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.user_1 = User()
        cls.user_1.first_name = "Greg"
        cls.user_1.last_name = "Rhys"
        cls.user_1.email = "greg.rhys@mail.com"
        cls.user_1.password = "root"

    @classmethod
    def tearDownClass(cls):
        del cls.user_1
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass

    def test_style_check(self):
        """
        Tests pep8 style
        """
        style = pep8.StyleGuide(quiet=True)
        p = style.check_files(['models/user.py'])
        self.assertEqual(p.total_errors, 0, "fix pep8")

    def test_is_subclass(self):
        self.assertEqual(issubclass(self.user_1.__class__, BaseModel), True)

    def test_checking_for_functions(self):
        self.assertIsNotNone(User.__doc__)

    def test_attributes(self):
        self.assertTrue('email' in self.user_1.__dict__)
        self.assertTrue('first_name' in self.user_1.__dict__)
        self.assertTrue('last_name' in self.user_1.__dict__)
        self.assertTrue('password' in self.user_1.__dict__)
        self.assertTrue('id' in self.user_1.__dict__)
        self.assertTrue('created_at' in self.user_1.__dict__)
        self.assertTrue('updated_at' in self.user_1.__dict__)
    
    def test_attributes_are_strings(self):
        self.assertEqual(type(self.user_1.email), str)
        self.assertEqual(type(self.user_1.first_name), str)
        self.assertEqual(type(self.user_1.last_name), str)
        self.assertEqual(type(self.user_1.password), str)
    
    def test_save(self):
        self.user_1.save()
        self.assertNotEqual(self.user_1.created_at, self.user_1.updated_at)

    def test_to_dict(self):
        self.assertEqual('to_dict' in dir(self.user_1), True)


if __name__ == "__main__":
    unittest.main()
