#! usr/bin/python3
__author__ = 'alexander'

import sys

sys.path.append('..')
from timechannel import timechannel
import unittest
import datetime as dt


class test_Time(unittest.TestCase):
    def setUp(self):
        self.test_timechannel = timechannel()

    def test_main(self):
        self.test_timechannel.time_dict[0].append((dt.time(16, 00), False))
        self.test_timechannel.time_dict[0].append((dt.time(18, 00), True))
        self.test_timechannel.time_dict[0].append((dt.time(20, 00), False))
        self.test_timechannel.time_dict[0].append((dt.time(22, 00), True))
        self.assertTrue(self.test_timechannel.check_if_true_test(18, 1, 0))
        self.assertTrue(self.test_timechannel.check_if_true_test(19, 1, 0))
        self.assertFalse(self.test_timechannel.check_if_true_test(20, 1, 0))


    def test_sec(self):
        self.test_timechannel.time_dict[0] = [
            (dt.time(0, 0), True),
            (dt.time(3, 0), False),
            (dt.time(23, 0), True),
            (dt.time(14, 0), False),
            (dt.time(9, 0), True)
        ]
        self.assertTrue(self.test_timechannel.check_if_true_test(11, 1, 0))

if __name__ == '__main__':
    unittest.main()
