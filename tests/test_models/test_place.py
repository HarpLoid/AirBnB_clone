#!/usr/bin/python3
"""
Unittest for Place class
"""
import unittest
import os
import pep8
from models.place import Place
from models.base_model import BaseModel


class TestCity(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.place_1 = Place()
        cls.place_1.city_id = "Magina"
        cls.place_1.name = "Bologona"
        cls.place_1.user_id = "Dustin"
        cls.place_1.description = "Magnificent"
        cls.place_1.number_rooms = 0
        cls.place_1.number_bathrooms = 0
        cls.place_1.max_guest = 0
        cls.place_1.price_by_night = 0
        cls.place_1.latitude = 0.0
        cls.place_1.longitude = 0.0
        cls.place_1.amenity_ids = []

    @classmethod
    def tearDownClass(cls):
        del cls.place_1
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass

    def test_style_check(self):
        """
        Tests pep8 style
        """
        style = pep8.StyleGuide(quiet=True)
        p = style.check_files(['models/place.py'])
        self.assertEqual(p.total_errors, 0, "fix pep8")

    def test_is_subclass(self):
        self.assertEqual(issubclass(self.place_1.__class__,
                                    BaseModel), True)

    def test_checking_for_functions(self):
        self.assertIsNotNone(Place.__doc__)

    def test_attributes(self):
        self.assertTrue('id' in self.place_1.__dict__)
        self.assertTrue('created_at' in self.place_1.__dict__)
        self.assertTrue('updated_at' in self.place_1.__dict__)
        self.assertTrue('city_id' in self.place_1.__dict__)
        self.assertTrue('user_id' in self.place_1.__dict__)
        self.assertTrue('name' in self.place_1.__dict__)
        self.assertTrue('description' in self.place_1.__dict__)
        self.assertTrue('number_rooms' in self.place_1.__dict__)
        self.assertTrue('number_bathrooms' in self.place_1.__dict__)
        self.assertTrue('max_guest' in self.place_1.__dict__)
        self.assertTrue('price_by_night' in self.place_1.__dict__)
        self.assertTrue('latitude' in self.place_1.__dict__)
        self.assertTrue('longitude' in self.place_1.__dict__)
        self.assertTrue('amenity_ids' in self.place_1.__dict__)

    def test_attributes_are_strings(self):
        self.assertEqual(type(self.place_1.city_id), str)
        self.assertEqual(type(self.place_1.user_id), str)
        self.assertEqual(type(self.place_1.name), str)
        self.assertEqual(type(self.place_1.description), str)
        self.assertEqual(type(self.place_1.number_rooms), int)
        self.assertEqual(type(self.place_1.number_bathrooms), int)
        self.assertEqual(type(self.place_1.max_guest), int)
        self.assertEqual(type(self.place_1.price_by_night), int)
        self.assertEqual(type(self.place_1.latitude), float)
        self.assertEqual(type(self.place_1.longitude), float)
        self.assertEqual(type(self.place_1.amenity_ids), list)

    def test_save(self):
        self.place_1.save()
        self.assertNotEqual(self.place_1.created_at,
                            self.place_1.updated_at)

    def test_to_dict(self):
        self.assertEqual('to_dict' in dir(self.place_1), True)


if __name__ == "__main__":
    unittest.main()
