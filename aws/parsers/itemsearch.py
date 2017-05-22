from __future__ import unicode_literals

from collections import namedtuple

from .base import BaseElementWrapper, Bin
from .helpers import load_into
from .api_response import ApiResponse


class SearchBinSet(object):
    """
    Enum for search bin types.
    """
    SUBJECT = 'Subject'
    BRAND_NAME = 'BrandName'
    PRICE_RANGE = 'PriceRange'
    PERCENTAGE_OFF = 'PercentageOff'


class ItemSearchResponse(ApiResponse, BaseElementWrapper):
    @load_into(Bin)
    def search_bins(self, narrow_by=None):
        if narrow_by is not None:
            xpath = './a:Items/a:SearchBinSets/a:SearchBinSet[@NarrowBy="{}"]//a:Bin'.format(narrow_by)
        else:
            xpath = './a:Items/a:SearchBinSets/a:SearchBinSet//a:Bin'
        return self.xpath(xpath)
