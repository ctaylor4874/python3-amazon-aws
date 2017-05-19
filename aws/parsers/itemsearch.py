from __future__ import unicode_literals

from collections import namedtuple

from .base import BaseElementWrapper, OperationRequest, Items, Bin
from .helpers import first_element, parse_bool, load_into


ITEM_SEARCH_NAMESPACES = {
    'a': 'http://webservices.amazon.com/AWSECommerceService/2011-08-01'
}


class SearchBinSet(object):
    """
    Enum for search bin types.
    """
    SUBJECT = 'Subject'
    BRAND_NAME = 'BrandName'
    PRICE_RANGE = 'PriceRange'
    PERCENTAGE_OFF = 'PercentageOff'


class ItemSearchResponse(BaseElementWrapper):
    namespaces = ITEM_SEARCH_NAMESPACES

    @property
    @load_into(OperationRequest)
    @first_element
    def operation_request(self):
        return self.xpath('./a:OperationRequest')

    @property
    @load_into(Items)
    @first_element
    def items(self):
        return self.xpath('./a:Items')

    @load_into(Bin)
    def search_bins(self, narrow_by=None):
        if narrow_by is not None:
            xpath = './a:Items/a:SearchBinSets/a:SearchBinSet[@NarrowBy="{}"]//a:Bin'.format(narrow_by)
        else:
            xpath = './a:Items/a:SearchBinSets/a:SearchBinSet//a:Bin'
        return self.xpath(xpath)
