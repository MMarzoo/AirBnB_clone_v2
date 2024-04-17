#!/usr/bin/python3
""" """
from models.base_model import BaseModel
import unittest
import datetime
import uuid
import json
import os


class test_basemodel(unittest.TestCase):
    """ """

    def __init__(self, *args, **kwargs):
        """ """
        super().__init__(*args, **kwargs)
        self.name = 'BaseModel'
        self.value = BaseModel

    def setUp(self):
        """Setup tests"""
        self.file = 'hbnb.json'

    def tearDown(self):
        try:
            os.remove(self.file)
        except Exception:
            pass

    def test_default(self):
        """ """
        bm = self.value()
        self.assertEqual(type(bm), self.value)

    def test_kwargs(self):
        """ """
        bm = self.value()
        copy = bm.to_dict()
        new = BaseModel(**copy)
        self.assertFalse(new is bm)

    def test_kwargs_int(self):
        """ """
        bm = self.value()
        copy = bm.to_dict()
        copy.update({1: 2})
        with self.assertRaises(TypeError):
            new = BaseModel(**copy)

    def test_save(self):
        """Testing save"""
        bm = self.value()
        bm.save()
        key = self.name + "." + bm.id
        with open('hbnb.json', 'r') as f:
            j = json.load(f)
            self.assertEqual(j[key], bm.to_dict())

    def test_str(self):
        """ """
        bm = self.value()
        self.assertEqual(
            str(bm), '[{}] ({}) {}'.format(self.name, bm.id, bm.__dict__)
        )

    def test_todict(self):
        """ """
        bm = self.value()
        n = bm.to_dict()
        self.assertEqual(bm.to_dict(), n)

    def test_kwargs_none(self):
        """ """
        n = {None: None}
        with self.assertRaises(TypeError):
            new = self.value(**n)

    def test_kwargs_one(self):
        """ """
        n = {"Name": "test"}
        with self.assertRaises(KeyError):
            new = self.value(**n)

    def test_id(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.id), str)

    def test_created_at(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.created_at), datetime.datetime)

    def test_updated_at(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.updated_at), datetime.datetime)
        n = new.to_dict()
        new = BaseModel(**n)
        self.assertNotEqual(new.created_at, new.updated_at)
