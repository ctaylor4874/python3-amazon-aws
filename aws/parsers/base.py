from functools import partial
from collections import namedtuple
import warnings
import re

from lxml import etree

from .helpers import first_element, load_into, parse_bool


ITEM_SEARCH_NAMESPACES = {
    'a': 'http://webservices.amazon.com/AWSECommerceService/2011-08-01'
}


class XMLWarning(Warning):
    pass


class BaseElementWrapper(object):

    namespaces = ITEM_SEARCH_NAMESPACES

    def __init__(self, element, *args, **kwargs):
        self.element = element
        if kwargs.get('namespaces'):
            self.namespaces = kwargs['namespaces']
        if element is None:
            self.xpath = lambda *args, **kwargs: None
        else:
            self.xpath = partial(self.element.xpath, namespaces=self.namespaces)
            self._element_validation()

    def __nonzero__(self):
        return self.element is not None

    def __bool__(self):
        return self.__nonzero__()

    def _element_validation(self):
        self._warn_if_no_namespace()

    def _warn_if_no_namespace(self):
        s = etree.tostring(self.element)
        if not re.findall(br'\sxmlns=\".*?\"', s):
            warnings.warn('Document is missing a namespace. Parsers may not behave as expected.', category=XMLWarning)

    def to_string(self):
        return etree.tostring(self.element).decode('utf-8')

    @classmethod
    def from_string(cls, xml_string, *args, **kwargs):
        tree = etree.fromstring(xml_string)
        return cls(tree, *args, **kwargs)


class ErrorElement(BaseElementWrapper):

    def __init__(self, element, *args, **kwargs):
        self.namespaces = kwargs.pop('namespaces', {})
        super(ErrorElement, self).__init__(element)

    @property
    @first_element
    def code(self):
        return self.xpath('./a:Code/text()')

    @property
    @first_element
    def message(self):
        return self.xpath('./a:Message/text()')


class ItemSearchErrorResponse(BaseElementWrapper):

    namespaces = {
        'a': 'http://ecs.amazonaws.com/doc/2005-10-05/'
    }

    @property
    @first_element
    def request_id(self):
        return self.xpath('./a:RequestID/text()')

    @property
    @first_element
    def _error(self):
        return self.xpath('./a:Error')

    @property
    def error(self):
        return ErrorElement(self._error, namespaces=self.namespaces)

    def raise_for_error(self):
        # Prevent issues with recursive imports
        from .errors import get_error
        if self.error:
            Err = get_error(self.error.code)
            raise Err(self.error.code, self.error.message)

    def __nonzero__(self):
        return bool(self.error)

    def __bool__(self):
        return self.__nonzero__()


def raise_error_for_content(f):
    def inner(*args, **kwargs):
        content = f(*args, **kwargs)
        potential_err = ItemSearchErrorResponse.from_string(content)
        potential_err.raise_for_error()
        return content
    return inner


class KeyValuePair(BaseElementWrapper):
    """
    Used to encapsulate elements which only have a Name and Value property.
    Examples:
        Header
        Argument
    """
    namespaces = ITEM_SEARCH_NAMESPACES

    KeyValue = namedtuple('KeyValue', ['key', 'value'])

    @property
    @first_element
    def name(self):
        return self.xpath('./@Name')

    @property
    @first_element
    def value(self):
        return self.xpath('./@Value')

    def as_tuple(self):
        return self.KeyValue(self.name, self.value)

    def __unicode__(self):
        return '{}={}'.format(self.name, self.value)

    def __str__(self):
        return self.__unicode__()

    def __repr__(self):
        return '<{} name={} value={}>'.format(self.__class__.__name__, self.name, self.value)


class CurrencyElement(BaseElementWrapper):

    @property
    @first_element
    def amount(self):
        return self.xpath('./a:Amount/text()')

    @property
    @first_element
    def currency_code(self):
        return self.xpath('./a:CurrencyCode/text()')

    @property
    @first_element
    def formatted_price(self):
        return self.xpath('./a:FormattedPrice/text()')


class OfferSummary(BaseElementWrapper):
    namespaces = ITEM_SEARCH_NAMESPACES

    @property
    @load_into(CurrencyElement, namespaces=namespaces)
    @first_element
    def lowest_new_price(self):
        return self.xpath('./a:LowestNewPrice')

    @property
    @load_into(CurrencyElement, namespaces=namespaces)
    @first_element
    def lowest_used_price(self):
        return self.xpath('./a:LowestUsedPrice')

    @property
    @first_element
    def total_new(self):
        return self.xpath('./a:TotalNew/text()')

    @property
    @first_element
    def total_used(self):
        return self.xpath('./a:TotalUsed/text()')

    @property
    @first_element
    def total_collectible(self):
        return self.xpath('./a:TotalCollectible/text()')

    @property
    @first_element
    def total_refurbished(self):
        return self.xpath('./a:TotalRefurbished/text()')


class OfferListing(BaseElementWrapper):
    namespaces = ITEM_SEARCH_NAMESPACES

    @property
    @first_element
    def offer_listing_id(self):
        return self.xpath('./a:OfferListingId/text()')

    @property
    @load_into(CurrencyElement, namespaces=namespaces)
    @first_element
    def price(self):
        return self.xpath('./a:Price')

    @property
    @load_into(CurrencyElement, namespaces=namespaces)
    @first_element
    def amount_saved(self):
        return self.xpath('./a:AmountSaved')

    @property
    @first_element
    def percentage_saved(self):
        return self.xpath('./a:PercentageSaved/text()')

    @property
    @first_element
    def availability(self):
        return self.xpath('./a:Availability/text()')

    # ToDo: AvailabilityAttributes
    # ToDo: IsEligibleForSuperSaverShipping
    # ToDo: IsEligibleForPrime


class Image(BaseElementWrapper):
    namespaces = ITEM_SEARCH_NAMESPACES

    @property
    @first_element
    def url(self):
        return self.xpath('./a:URL/text()')

    @property
    @first_element
    def height(self):
        return self.xpath('./a:Height/text()')

    @property
    @first_element
    def width(self):
        return self.xpath('./a:Width/text()')


class ImageSet(BaseElementWrapper):

    namespaces = ITEM_SEARCH_NAMESPACES

    @property
    @load_into(Image)
    @first_element
    def swatch_image(self):
        return self.xpath('./a:SwatchImage')

    @property
    @load_into(Image)
    @first_element
    def small_image(self):
        return self.xpath('./a:SmallImage')

    @property
    @load_into(Image)
    @first_element
    def thumbnail_image(self):
        return self.xpath('./a:ThumbnailImage')

    @property
    @load_into(Image)
    @first_element
    def tiny_image(self):
        return self.xpath('./a:TinyImage')

    @property
    @load_into(Image)
    @first_element
    def medium_image(self):
        return self.xpath('./a:MediumImage')

    @property
    @load_into(Image)
    @first_element
    def large_image(self):
        return self.xpath('./a:LargeImage')


class Offer(BaseElementWrapper):
    """
    Offer has been condensed to "flatten" the xml. Amazon still retains the old layout even though they
    will only ever bring at most 1 offer back. So by condensing this it saves a lot of development time.
    """
    namespaces = ITEM_SEARCH_NAMESPACES

    @property
    @first_element
    def merchant(self):
        return self.xpath('./a:Merchant/a:Name/text()')

    @property
    @first_element
    def condition(self):
        return self.xpath('./a:OfferAttributes/a:Condition/text()')

    @property
    @load_into(OfferListing)
    @first_element
    def _offer(self):
        return self.xpath('./a:OfferListing')

    @property
    def price(self):
        return self._offer.price

    @property
    def amount_saved(self):
        return self._offer.amount_saved

    @property
    def percentage_saved(self):
        return self._offer.percentage_saved

    @property
    def availability(self):
        return self._offer.availability


class OperationRequest(BaseElementWrapper):
    namespaces = ITEM_SEARCH_NAMESPACES

    @property
    def http_headers(self):
        return [KeyValuePair(x).as_tuple() for x in self.xpath('./a:HTTPHeaders//a:Header')]

    @property
    @first_element
    def request_id(self):
        return self.xpath('./a:RequestId/text()')

    @property
    def arguments(self):
        return [KeyValuePair(x).as_tuple() for x in self.xpath('./a:Arguments//a:Argument')]

    @property
    @first_element
    def request_processing_time(self):
        return self.xpath('./a:RequestProcessingTime/text()')


class ItemSearchRequest(BaseElementWrapper):
    namespaces = ITEM_SEARCH_NAMESPACES

    @property
    @first_element
    def brand(self):
        return self.xpath('./a:Brand/text()')

    @property
    @first_element
    def item_page(self):
        return self.xpath('./a:ItemPage/text()')

    @property
    def response_groups(self):
        return self.xpath('.//a:ResponseGroup/text()')

    @property
    @first_element
    def search_index(self):
        return self.xpath('./a:SearchIndex/text()')


class Request(BaseElementWrapper):

    namespaces = ITEM_SEARCH_NAMESPACES

    @property
    @parse_bool
    @first_element
    def is_valid(self):
        return self.xpath('./a:IsValid/text()')

    @property
    @load_into(ItemSearchRequest)
    @first_element
    def item_search_request(self):
        return self.xpath('./a:ItemSearchRequest')

    @property
    @load_into(ErrorElement, namespaces=namespaces)
    def errors(self):
        return self.xpath('./a:Errors//a:Error')


class ItemAttributes(BaseElementWrapper):

    namespaces = ITEM_SEARCH_NAMESPACES

    @property
    @first_element
    def brand(self):
        return self.xpath('./a:Brand/text()')

    @property
    @first_element
    def manufacturer(self):
        return self.xpath('./a:Manufacturer/text()')

    @property
    @first_element
    def title(self):
        return self.xpath('./a:Title/text()')

    @property
    @first_element
    def color(self):
        return self.xpath('./a:Color/text()')

    @property
    @first_element
    def label(self):
        return self.xpath('./a:Label/text()')

    @property
    @first_element
    def publisher(self):
        return self.xpath('./a:Publisher/text()')


class Item(BaseElementWrapper):

    namespaces = ITEM_SEARCH_NAMESPACES

    @property
    @first_element
    def asin(self):
        return self.xpath('./a:ASIN/text()')

    @property
    @first_element
    def sales_rank(self):
        return self.xpath('./a:SalesRank/text()')

    @property
    @load_into(ItemAttributes)
    @first_element
    def item_attributes(self):
        return self.xpath('./a:ItemAttributes')

    @property
    @load_into(Offer)
    @first_element
    def offer(self):
        return self.xpath('./a:Offers/a:Offer')

    @property
    @load_into(OfferSummary)
    @first_element
    def offer_summary(self):
        return self.xpath('./a:OfferSummary')

    @property
    @load_into(Image)
    @first_element
    def small_image(self):
        return self.xpath('./a:SmallImage')

    @property
    @load_into(Image)
    @first_element
    def medium_image(self):
        return self.xpath('./a:MediumImage')

    @property
    @load_into(Image)
    @first_element
    def large_image(self):
        return self.xpath('./a:LargeImage')

    @load_into(ImageSet)
    @first_element
    def image_set(self, category):
        return self.xpath('./a:ImageSets/a:ImageSet[@Category="{}"]'.format(category))

    @property
    def image_set_variant(self):
        return self.image_set('variant')

    @property
    def image_set_primary(self):
        return self.image_set('primary')

    def __unicode__(self):
        return self.asin

    def __str__(self):
        return self.__unicode__()

    def __repr__(self):
        return '<{} asin={}>'.format(self.__class__.__name__, self.asin)


class Items(BaseElementWrapper):

    namespaces = ITEM_SEARCH_NAMESPACES

    @property
    @load_into(Request)
    @first_element
    def request(self):
        return self.xpath('./a:Request')

    @property
    @first_element
    def total_results(self):
        return self.xpath('./a:TotalResults/text()')

    @property
    @first_element
    def total_pages(self):
        return self.xpath('./a:TotalPages/text()')

    @property
    @first_element
    def more_search_results_url(self):
        return self.xpath('./a:MoreSearchResultsUrl/text()')

    @property
    def items(self):
        return [Item(x) for x in self.xpath('.//a:Item')]


class BinParameter(KeyValuePair):
    namespaces = ITEM_SEARCH_NAMESPACES

    @property
    @first_element
    def name(self):
        return self.xpath('./a:Name/text()')

    @property
    @first_element
    def value(self):
        return self.xpath('./a:Value/text()')


class Bin(BaseElementWrapper):
    namespaces = ITEM_SEARCH_NAMESPACES

    @property
    @first_element
    def bin_name(self):
        return self.xpath('./a:BinName/text()')

    @property
    @first_element
    def bin_item_count(self):
        return self.xpath('./a:BinItemCount/text()')

    @property
    @load_into(BinParameter)
    @first_element
    def bin_parameter(self):
        return self.xpath('./a:BinParameter')

    def __unicode__(self):
        return self.bin_name

    def __str__(self):
        return self.__unicode__()

    def __repr__(self):
        return '<{} bin_name={} bin_item_count={} bin_id={}>'.format(
            self.__class__.__name__,
            self.bin_name,
            self.bin_item_count,
            self.bin_parameter.value
        )

    def as_request_params(self):
        return {
            self.bin_parameter.name: self.bin_parameter.value
        }