from unittest import TestCase

from kindle_version_cache import KindleVersionCache


class TestKindleVersionCache(TestCase):

    def test_cache_object(self):
        cache = KindleVersionCache(servers=['127.0.0.1'], key_prefix='jp:')

        cache.set_cached_items({
            'hoge': {'asin': 'foo', 'title': 'FOO!'},
            'fuga': None,
            })

        self.assertEqual(cache.get_cached_items(['hoge', 'fuga', 'hige']),
            {
                'hoge': {'asin': 'foo', 'title': 'FOO!'},
                'fuga': None,
            })
