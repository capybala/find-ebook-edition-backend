#coding: utf-8
from __future__ import unicode_literals

import re
import logging

from kindle_version_cache import KindleVersionCache
from api_wrapper import AmazonWrapper, AmazonException

VALID_ASIN_RE = re.compile(r'^\w{10}$')

logger = logging.getLogger(__name__)


class KindleVersionFinder(object):

    def __init__(self, access_key, secret_key, associate_tag, country, cache_args=None):
        if cache_args:
            self.cache = KindleVersionCache(key_prefix=('%s:' % country), **cache_args)
        else:
            self.cache = None

        self.api = AmazonWrapper(access_key, secret_key, associate_tag, country)

    def _cache_enabled(self):
        return self.cache is not None

    def find_kindle_version(self, asins):
        self.validate_asins(asins)

        try:
            cached_items = self.get_cached_items(asins)
            logger.debug('Retrieved from cache: %s' % cached_items)
            remaining_asins = [asin for asin in asins if asin not in cached_items]

            if remaining_asins:
                kindle_versions = self.get_kindle_versions(remaining_asins)
                self.set_cached_items(kindle_versions)
            else:
                kindle_versions = {}

            kindle_versions.update(cached_items)

            response_items = []
            for asin in asins:  # preserve asins' order
                response_items.append({
                    'asin': asin,
                    'kindle': kindle_versions[asin],
                })

            return response_items
        except AmazonException:
            raise

    def validate_asins(self, asins):
        if len(asins) > 10:
            raise Exception('Too many asins')

        if any(not VALID_ASIN_RE.search(asin) for asin in asins):
            raise Exception('Invalid asin exists')

    def get_kindle_versions(self, asins):
        """
        Retrieve a dict whose form is {ASIN => (a dict of Kindle edition's detail OR None)}
        """

        # a dcit {ASIN => None}
        response_items = dict(zip(asins, [None] * len(asins)))

        # Retrieve alternate versions
        map_asin_to_kindle_asin = self.api.get_alternate_versions(asins)

        # Retrieve details of Kindle editions
        kindle_asins = map_asin_to_kindle_asin.values()

        if kindle_asins:
            kindle_items = self.api.get_item_details(kindle_asins)

            for asin, kindle_asin in map_asin_to_kindle_asin.items():
                response_items[asin] = kindle_items[kindle_asin]

        return response_items

    def get_cached_items(self, asins):
        """
        Retrieve a dict whose form is {ASIN => item details}.
        The dict does not contain keys which don't exist in the cache.
        """

        if not self._cache_enabled():
            return {}

        return self.cache.get_cached_items(asins)

    def set_cached_items(self, items):
        if not self._cache_enabled():
            return  # do nothing

        self.cache.set_cached_items(items)
