from flask import Flask
import app
import unittest

class MyAppUnitTestCase(unittest.TestCase):
    """ Unit Test Cases for app.py survey app"""

    def test_select_survey(self):
        client = app.test_client()
        result = client.get('/')
        self.assertEquals(result.status_code, 200)
        self.assertIn(b'satisfaction', result.data)
