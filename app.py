#coding: utf-8
from __future__ import unicode_literals

import re
import os
import json
import logging
import traceback

from flask import Flask, request
from kindle_version_finder import KindleVersionFinder

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

VALID_COUNTRY_RE = re.compile(r'^(ca|de|fr|jp|uk|us|cn)$')
MEMCACHE_SERVERS = [os.environ.get('MEMCACHIER_SERVERS')]
MEMCACHE_USERNAME = os.environ.get('MEMCACHIER_USERNAME')
MEMCACHE_PASSWORD = os.environ.get('MEMCACHIER_PASSWORD')

ACCESS_KEY = os.environ.get('AMAZON_ACCESS_KEY')
SECRET_KEY = os.environ.get('AMAZON_SECRET_KEY')
ASSOCIATE_TAG = os.environ.get('AMAZON_ASSOCIATE_TAG')


@app.route('/')
def hello():
    return 'Hello World!'


@app.route('/kindle_versions')
def kindle_versions():
    try:
        country = request.args.get('country')
        if not VALID_COUNTRY_RE.search(country):
            raise Exception('Invalid country')

        asins = request.args.get('asin', '').split(',')
        finder = KindleVersionFinder(ACCESS_KEY, SECRET_KEY, ASSOCIATE_TAG,
                                     country, cache_args={
                                         'servers': MEMCACHE_SERVERS,
                                         'username': MEMCACHE_USERNAME,
                                         'password': MEMCACHE_PASSWORD,
                                         'binary': True,
                                     })

        items = finder.find_kindle_version(asins)
        status = 200
    except Exception, ex:
        app.logger.error('Error in calling API. %s: %s' % (
            ex.__class__.__name__, ex))
        app.logger.error(traceback.format_exc())
        items = {'error': 1}
        status = 400

    return json.dumps(items), status


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG') in ('1', 'True')
    if debug:
        app.run(host='127.0.0.1', port=port, debug=True)
    else:
        app.run(host='0.0.0.0', port=port)
