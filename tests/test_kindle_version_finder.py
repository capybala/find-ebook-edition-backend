#coding: utf-8

import os
from unittest import TestCase

from kindle_version_finder import KindleVersionFinder

ACCESS_KEY = os.environ.get('AMAZON_ACCESS_KEY')
SECRET_KEY = os.environ.get('AMAZON_SECRET_KEY')
ASSOCIATE_TAG = os.environ.get('AMAZON_ASSOCIATE_TAG')


class TestKindleVersionFinder(TestCase):

    def test_find_kindle_version(self):

        finder = KindleVersionFinder(ACCESS_KEY, SECRET_KEY, ASSOCIATE_TAG, 'jp')

        asins = [
            '4274068854',  # a book with kindle version
            '4873115736',  # a book without kindle version
            'B009TPQVLY',  # kindle book
            'B0095D9XS8',  # not a book
        ]

        items = finder.find_kindle_version(asins)

        self.assertEqual(items[0]['asin'], '4274068854')
        self.assertEqual(items[0]['kindle']['asin'], 'B009RO80XY')
        self.assertTrue(items[0]['kindle']['url'].startswith('http://www.amazon.co.jp/%E3%81%99%E3%81%94%E3%81%84Haskell%E3%81%9F%E3%81%AE%E3%81%97%E3%81%8F%E5%AD%A6%E3%81%BC%E3%81%86%EF%BC%81-Miran-Lipovaca-ebook/dp/B009RO80XY'))
        self.assertTrue('orangain-22' in items[0]['kindle']['url'])
        self.assertEqual(items[0]['kindle']['title'], u"すごいHaskellたのしく学ぼう！")

        self.assertEqual(items[1], {"asin": "4873115736", "kindle": None})
        self.assertEqual(items[2], {"asin": "B009TPQVLY", "kindle": None})
        self.assertEqual(items[3], {"asin": "B0095D9XS8", "kindle": None})

    def test_jp(self):
        finder = KindleVersionFinder(ACCESS_KEY, SECRET_KEY, ASSOCIATE_TAG, 'jp')
        asins = ['0470747994']
        items = finder.find_kindle_version(asins)

        self.assertEqual(items[0]['kindle']['asin'], 'B005UQLJ4A')
        self.assertTrue(items[0]['kindle']['url'].startswith('http://www.amazon.co.jp/'))

    def test_us(self):
        finder = KindleVersionFinder(ACCESS_KEY, SECRET_KEY, ASSOCIATE_TAG, 'us')
        asins = ['0470747994']
        items = finder.find_kindle_version(asins)

        self.assertEqual(items[0]['kindle']['asin'], 'B005UQLJ4A')
        self.assertTrue(items[0]['kindle']['url'].startswith('http://www.amazon.com/'))

    def test_uk(self):
        finder = KindleVersionFinder(ACCESS_KEY, SECRET_KEY, ASSOCIATE_TAG, 'uk')
        asins = ['0470747994']
        items = finder.find_kindle_version(asins)

        self.assertEqual(items[0]['kindle']['asin'], 'B005UQLJ4A')
        self.assertTrue(items[0]['kindle']['url'].startswith('http://www.amazon.co.uk/'))

    def test_de(self):
        finder = KindleVersionFinder(ACCESS_KEY, SECRET_KEY, ASSOCIATE_TAG, 'de')
        asins = ['0470747994']
        items = finder.find_kindle_version(asins)

        self.assertEqual(items[0]['kindle']['asin'], 'B005UQLJ4A')
        self.assertTrue(items[0]['kindle']['url'].startswith('http://www.amazon.de/'))

    def test_cn(self):
        finder = KindleVersionFinder(ACCESS_KEY, SECRET_KEY, ASSOCIATE_TAG, 'cn')
        asins = ['B003H9NHVU']
        items = finder.find_kindle_version(asins)

        self.assertEqual(items[0]['kindle']['asin'], 'B00AATSWWE')
        self.assertTrue(items[0]['kindle']['url'].startswith('http://www.amazon.cn/'))

    def test_ca(self):
        finder = KindleVersionFinder(ACCESS_KEY, SECRET_KEY, ASSOCIATE_TAG, 'ca')
        asins = ['0470747994']
        items = finder.find_kindle_version(asins)

        self.assertEqual(items[0]['kindle']['asin'], 'B005UQLJ4A')
        self.assertTrue(items[0]['kindle']['url'].startswith('http://www.amazon.ca/'))
