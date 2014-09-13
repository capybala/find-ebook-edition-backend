from unittest import TestCase

from utils import to_bytes, to_str


class TestUtils(TestCase):

    def test_bytes(self):
        self.assertEqual(to_bytes(b'Should be bytes \xe3\x81\xa0\xe3\x82\x88'),
                         b'Should be bytes \xe3\x81\xa0\xe3\x82\x88')
        self.assertEqual(to_bytes('Should be bytes だよ'),
                         b'Should be bytes \xe3\x81\xa0\xe3\x82\x88')

    def test_str(self):
        self.assertEqual(to_str(b'Should be (Python 3) str \xe3\x81\xa0\xe3\x82\x88'),
                         'Should be (Python 3) str だよ')
        self.assertEqual(to_str('Should be (Python 3) str だよ'),
                         'Should be (Python 3) str だよ')
