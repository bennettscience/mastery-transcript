import unittest

from app.utils import is_json


class TestIsJson(unittest.TestCase):
    def test_good_input(self):
        data = '{"foo": "bar"}'
        req = is_json(data)
        self.assertTrue(req)

    def test_bad_input(self):
        data = "this is a string"
        req = is_json(data)
        self.assertFalse(req)

    def test_submit_object(self):
        data = {"public": "true"}
        req = is_json(data)
        self.assertTrue(req)
