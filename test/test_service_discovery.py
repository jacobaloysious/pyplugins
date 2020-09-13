import sys
import os
import unittest

#Hack clean up later using a test.context class
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', r"src")))

from iplugin import IPlugin
from service_discovery import ServiceDiscovery

'''
How to run the tests:

nosetests -v .\test\test_service_discovery.py

https://docs.python.org/3/library/unittest.html#unittest.TestCase.debug
'''

class Test_ServiceDiscovery(unittest.TestCase):

    def test_topic_registration(self):
        ser_dis = ServiceDiscovery()
        self.assertEqual(len(ser_dis.plugin_topic_instance_map), 3)
        self.assertIsInstance(ser_dis.plugin_topic_instance_map['Add'], IPlugin)
        self.assertIsInstance(ser_dis.plugin_topic_instance_map['Sample'], IPlugin)      
    
    def test_trigger_plugin(self):
        ser_dis = ServiceDiscovery()
        
        # Valid topic
        ser_dis.execute("Sample", [1,2,3,4])

        # InValid Throws exception
        with self.assertRaises(Exception) as context:
            ser_dis.execute("Unknown", "argument")
        
        self.assertTrue('Topic: Unknown is not registered' in str(context.exception))

    def test_cal_plugin_add_func(self):
        # Arrange
        ser_dis = ServiceDiscovery()
        
        # Action
        result = ser_dis.execute("Add", [1,2])

        # Assert
        self.assertEqual(result, 3)

    def test_sample_plugin(self):
        # Arrange
        ser_dis = ServiceDiscovery()
        
        # Action
        result = ser_dis.execute("Sample", [1,2,3,4,5,6,7])

        # Assert
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], 3)
