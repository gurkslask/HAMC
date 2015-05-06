#! usr/bin/python3
__author__ = 'alexander'

import sys

sys.path.append('..')
import unittest
from cold_retain import cold_retain, cold_retain_load
import datetime as dt

class classwithcoldretain(object):

    def coldretainload(self):
        self.__dict__.update(cold_retain_load(self))
    def __init__(self):
        self.val = 42
    def change(self):
        self.val = 84
    def coldretain(self, list_with_vars):
        cold_retain(self, list_with_vars)

class test_ColdRetain(unittest.TestCase):
    def setUp(self):
        self.a_class = classwithcoldretain()

    def test_main(self):
        self.a_class.change()
        self.assertEqual(self.a_class.val, 84)
        self.temp = ['val']
        self.a_class.coldretain(self.temp)
        self.a_class = classwithcoldretain()
        self.assertEqual(self.a_class.val, 42)
        self.a_class.coldretainload()
        self.assertEqual(self.a_class.val, 84)

if __name__ == '__main__':
    unittest.main()
