from __future__ import unicode_literals

from collections import namedtuple

from .base import BaseElementWrapper, OperationRequest, Items, Bin
from .helpers import first_element, load_into

ITEM_SEARCH_NAMESPACES = {
    'a': 'http://webservices.amazon.com/AWSECommerceService/2011-08-01'
}


class ApiResponse(BaseElementWrapper):
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
