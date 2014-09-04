#coding: utf-8
from __future__ import unicode_literals, print_function

import logging

import bottlenose
from lxml import etree, objectify

from utils import to_str


KINDLE_BINDINGS = (
    'Kindle版',        # jp, cn
    'Kindle Edition',  # us, uk, ca, de
    'Format Kindle',   # fr
)
# Confirmed by http://www.amazon.*/dp/B005UQLJ4A/

logger = logging.getLogger(__name__)


class AmazonException(Exception):
    pass


class AmazonWrapper(object):

    def __init__(self, access_key, secret_key, associate_tag, region):
        self.api = bottlenose.Amazon(access_key, secret_key, associate_tag,
                                     Region=region.upper())

    def get_alternate_versions(self, asins):
        """
        Retrieve a dict whose form is {ASIN => ASIN of Kindle edition}
        The dict does not contain the keys of items which does not have a Kindle edition.

        asins: list of ASINs
        """

        asins_text = ','.join(asins)
        logger.debug('Caling API for AlternateVersions. asins: %s' % asins_text)
        response = self.api.ItemLookup(ItemId=asins_text,
                                       ResponseGroup='AlternateVersions')
        root = _parse_response(response)
        #print(etree.tostring(response, pretty_print = True))

        alternate_asins = {}
        for item in root.Items.Item:
            asin = item.ASIN.text
            alternate_asin = None

            #print(item.ItemAttributes.Title.text.encode('utf-8'))
            if hasattr(item, 'AlternateVersions'):
                for alternate_version in item.AlternateVersions.AlternateVersion:
                    if alternate_version.Binding in KINDLE_BINDINGS:
                        # When Kindle edtion exists
                        alternate_asin = to_str(alternate_version.ASIN.text)
                        break

            if alternate_asin:
                alternate_asins[asin] = alternate_asin

        return alternate_asins

    def get_item_details(self, asins):
        """
        Retrieve a dict whose form is {ASIN => dict of Item detail}
        """

        asins_text = ','.join(asins)
        logger.debug('Caling API for Small. asins: %s' % asins_text)
        response = self.api.ItemLookup(ItemId=asins_text, ResponseGroup='Small')
        root = _parse_response(response)
        #print(etree.tostring(response, pretty_print = True))

        items = {}
        for item in root.Items.Item:
            asin = to_str(item.ASIN.text)
            items[asin] = {
                'asin': asin,
                'title': to_str(item.ItemAttributes.Title.text),
                'url': to_str(item.DetailPageURL.text),
            }

        return items


def _parse_response(response_text):
    root = objectify.fromstring(response_text)
    if root.Items.Request.IsValid == 'False':
        raise AmazonException(
            "Error: '{0}', '{1}'".format(
                root.Items.Request.Errors.Error.Code,
                root.Items.Request.Errors.Error.Message))
    if not hasattr(root.Items, 'Item'):
        raise AmazonException("Items not found: '{0}'".format(
            etree.tostring(root, pretty_print=True)))

    return root
