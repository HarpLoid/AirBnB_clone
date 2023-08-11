#!/usr/bin/python3
"""
Unittest for City class
"""
import unittest
import os
import pep8
from models.city import City
from models.base_model import BaseModel


class TestCity(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.city_1 = City()
        cls.city_1.name = "New York"
        cls.city_1.state_id = "NY"

    @classmethod
    def tearDownClass(cls):
        del cls.city_1
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass

    def test_style_check(self):
        """
        Tests pep8 style
        """
        style = pep8.StyleGuide(quiet=True)
        p = style.check_files(['models/city.py'])
        self.assertEqual(p.total_errors, 0, "fix pep8")

    def test_is_subclass(self):
        self.assertEqual(issubclass(self.city_1.__class__, BaseModel), True)

    def test_checking_for_functions(self):
        self.assertIsNotNone(City.__doc__)

    def test_attributes(self):
        self.assertTrue('id' in self.city_1.__dict__)
        self.assertTrue('created_at' in self.city_1.__dict__)
        self.assertTrue('updated_at' in self.city_1.__dict__)
        self.assertTrue('name' in self.city_1.__dict__)
        self.assertTrue('state_id' in self.city_1.__dict__)
    
    def test_attributes_are_strings(self):
        self.assertEqual(type(self.city_1.name), str)
        self.assertEqual(type(self.city_1.state_id), str)
    
    def test_save(self):
        self.city_1.save()
        self.assertNotEqual(self.city_1.created_at, self.city_1.updated_at)

    def test_to_dict(self):
        self.assertEqual('to_dict' in dir(self.city_1), True)


if __name__ == "__main__":
    unittest.main()
