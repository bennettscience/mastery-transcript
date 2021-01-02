import unittest

from app.utils import is_json


class TestIsJson(unittest.TestCase):
    def test_good_json(self):
        data = '{"foo": "bar"}'
        req = is_json(data)
        self.assertTrue(req)

    def test_good_json_2(self):
        data = '{"public": "false"}'
        req = is_json(data)
        self.assertTrue(req)

    def test_bad_json(self):
        data = "this is a string"
        req = is_json(data)
        self.assertFalse(req)
