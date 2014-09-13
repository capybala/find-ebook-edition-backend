#coding: utf-8
from __future__ import unicode_literals, print_function

import json
import pylibmc
from utils import to_bytes, to_str

DEFAULT_CACHE_SECONDS = 60 * 60 * 24  # 1 day


class KindleVersionCache(object):

    def __init__(self, servers, username=None, password=None, binary=False,
                 key_prefix='', cache_seconds=DEFAULT_CACHE_SECONDS):

        self.cache = pylibmc.Client(servers=servers, binary=binary,
                                    username=username, password=password)
        self.key_prefix = to_bytes(key_prefix)  # key must be bytes
        self.cache_seconds = cache_seconds

    def get_cached_items(self, asins):
        """
        Retrieve a dict whose form is {ASIN => item details}.
        The dict does not contain keys which don't exist in the cache.
        """
        keys = [to_bytes(asin) for asin in asins]  # key must be bytes
        cached_json_items = self.cache.get_multi(keys, key_prefix=self.key_prefix)
        cached_items = {}
        for key, value in cached_json_items.items():
            # Although pylibmc automatically pickle dicts or objects,
            # JSON is more portable.
            cached_items[to_str(key)] = json.loads(value)  # convert key into (Py3) str

        return cached_items

    def set_cached_items(self, items):
        """
        items:
            {
                'asin with kindle edition': {
                    'asin': ...,
                    'title': ...,
                    'url': ...,
                },
                'asin without kindle edition': None,
            }
        """
        json_items = {}
        for key, value in items.items():
            json_items[to_bytes(key)] = json.dumps(value)  # key must be bytes

        self.cache.set_multi(json_items, time=self.cache_seconds, key_prefix=self.key_prefix)


if __name__ == '__main__':
    cache = KindleVersionCache(servers=['127.0.0.1'], key_prefix='jp:')

    cache.set_cached_items({
        'hoge': {'asin': 'foo', 'title': 'FOO!'},
        'fuga': None,
        })
    print(cache.get_cached_items(['hoge', 'fuga', 'hige']))
