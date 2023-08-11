#!/usr/bin/python3
"""
Unittest for Amenity class
"""
import unittest
import os
import pep8
from models.amenity import Amenity
from models.base_model import BaseModel


class TestAmenity(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.amenity_1 = Amenity()
        cls.amenity_1.name = "Hot Tub"

    @classmethod
    def tearDownClass(cls):
        del cls.amenity_1
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass

    def test_style_check(self):
        """
        Tests pep8 style
        """
        style = pep8.StyleGuide(quiet=True)
        p = style.check_files(['models/amenity.py'])
        self.assertEqual(p.total_errors, 0, "fix pep8")

    def test_is_subclass(self):
        self.assertEqual(issubclass(self.amenity_1.__class__, BaseModel), True)

    def test_checking_for_functions(self):
        self.assertIsNotNone(Amenity.__doc__)

    def test_attributes(self):
        self.assertTrue('id' in self.amenity_1.__dict__)
        self.assertTrue('created_at' in self.amenity_1.__dict__)
        self.assertTrue('updated_at' in self.amenity_1.__dict__)
        self.assertTrue('name' in self.amenity_1.__dict__)
    
    def test_attributes_are_strings(self):
        self.assertEqual(type(self.amenity_1.name), str)
    
    def test_save(self):
        self.amenity_1.save()
        self.assertNotEqual(self.amenity_1.created_at, self.amenity_1.updated_at)

    def test_to_dict(self):
        self.assertEqual('to_dict' in dir(self.amenity_1), True)


if __name__ == "__main__":
    unittest.main()
