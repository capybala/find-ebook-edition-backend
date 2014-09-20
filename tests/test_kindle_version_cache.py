from unittest import TestCase
import json

from kindle_version_cache import KindleVersionCache
from utils import to_bytes


class TestKindleVersionCache(TestCase):

    def test_cache_object(self):
        cache = KindleVersionCache(servers=['127.0.0.1'], key_prefix='test_cache_object:')

        cache.set_cached_items({
            'hoge': {'asin': 'foo', 'title': 'FOO!'},
            'fuga': None,
            })

        self.assertEqual(cache.get_cached_items(['hoge', 'fuga', 'hige']), {
            'hoge': {'asin': 'foo', 'title': 'FOO!'},
            'fuga': None,
        })

    def test_decode_bytes_json(self):
        cache = KindleVersionCache(servers=['127.0.0.1'], key_prefix='test_decode_bytes_json:')

        json_items = {
            'hoge': to_bytes(json.dumps({'asin': 'foo', 'title': '日本語'})),
            'fuga': to_bytes(json.dumps(None)),
        }
        cache.cache.set_multi(json_items, time=cache.cache_seconds, key_prefix=cache.key_prefix)

        self.assertEqual(cache.get_cached_items(['hoge', 'fuga', 'hige']), {
            'hoge': {'asin': 'foo', 'title': '日本語'},
            'fuga': None,
        })
