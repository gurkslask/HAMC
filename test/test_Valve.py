import sys
sys.path.append('..')
from OpenCloseValveClass import OpenCloseValve2
import unittest
import time


class test_Valve(unittest.TestCase):
    def setUp(self):
        self.ValveClass = OpenCloseValve2()
        self.IO_Dict = {
            'SV1_Open': {
                'Value': False},
            'SV1_Close': {
                'Value': False}
        }
        self.ValveClass.Open_IO = 'SV1_Open'
        self.ValveClass.Close_IO = 'SV1_Close'
        self.ValveClass.Name = 'SV1'

    def test_Open(self):
        #Open valve
        self.ValveClass.main(10, 30, self.IO_Dict)
        time.sleep(1)
        #Check that it opens
        self.assertTrue(self.IO_Dict['SV1_Open']['Value'])
        time.sleep(3)
        #Check that it stops opening after a time
        self.assertFalse(self.IO_Dict['SV1_Open']['Value'])

    def test_Close(self):
        #Close valve
        self.ValveClass.main(30, 10, self.IO_Dict)
        time.sleep(1)
        #Check that it closes
        self.assertTrue(self.IO_Dict['SV1_Close']['Value'])
        time.sleep(3)
        #Check that it stops closing after a time
        self.assertFalse(self.IO_Dict['SV1_Close']['Value'])

    def test_NotTheSame(self):
        #Open valve
        self.ValveClass.main(10, 30, self.IO_Dict)
        #Close valve
        self.ValveClass.main(30, 10, self.IO_Dict)
        time.sleep(0.5)
        #Check that it opens
        self.assertTrue(self.IO_Dict['SV1_Open']['Value'])
        #Check that it does NOT close
        self.assertFalse(self.IO_Dict['SV1_Close']['Value'])
        time.sleep(3.5)
        #Check that it stops opening after a time
        self.assertFalse(self.IO_Dict['SV1_Open']['Value'])
        #Check that it does NOT close
        self.assertFalse(self.IO_Dict['SV1_Close']['Value'])


if __name__ == '__main__':
    unittest.main()
