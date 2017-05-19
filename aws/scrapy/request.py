import datetime
import sys
from collections import defaultdict
from urllib import parse
import hmac
import base64
import hashlib

from scrapy import Request
from scrapy.exceptions import CloseSpider
from scrapy.utils.project import get_project_settings


def convert_to_gmtime(dt):
    """
    Convert the supplied date to GMT.
    :param dt:
    :return: parameter converted to GMT.
    :rtype: datetime.datetime
    """
    # Get the local time offset from gmt. Added 1 second to account for the time the computer takes to
    # generate utcnow and now.
    hr_diff = (((datetime.datetime.utcnow() - datetime.datetime.now()).seconds + 1) / 60) / 60
    return dt + datetime.timedelta(hours=hr_diff)


def formatted_amazon_datetime_str(dt=None):
    """
    Format a datetime object to amazon timestamp format spec. (YYYY-MM-DDThh:mm:ssZ) where T and Z are literals.
    :param dt: optional datetime to suppy. If none supplied, then use current datetime.
    :return: Formatted timestamp to use in request url.
    """
    dt = dt or datetime.datetime.now()
    gmtime = convert_to_gmtime(dt)
    return gmtime.strftime('%Y-%m-%dT%H:%M:%S.000Z')


def urlencode(query):
    """Encode a sequence of two-element tuples or dictionary into a URL query string.

    If any values in the query arg are sequences and doseq is true, each
    sequence element is converted to a separate parameter.

    If the query arg is a sequence of two-element tuples, the order of the
    parameters in the output will match the order of parameters in the
    input.

    Taken straight from urllib.urlencode. This is necessary because urllib.urlencode uses quote_plus but aws expects
    %20 instead of +.
    """

    if hasattr(query, "items"):
        # mapping objects
        query = query.items()
    else:
        # it's a bother at times that strings and string-like objects are
        # sequences...
        try:
            # non-sequence items should not work with len()
            # non-empty strings will fail this
            if len(query) and not isinstance(query[0], tuple):
                raise TypeError
                # zero-length sequences of all types will get here and succeed,
                # but that's a minor nit - since the original implementation
                # allowed empty dicts that type of behavior probably should be
                # preserved for consistency
        except TypeError:
            ty, va, tb = sys.exc_info()
            raise TypeError("not a valid non-string sequence or mapping object").with_traceback(tb)

    l = []
    for k, v in query:
        k = parse.quote(str(k), safe='')
        v = parse.quote(str(v), safe='')
        l.append(k + '=' + v)
    return '&'.join(l)


class AwsRequest(Request):
    def __init__(self, operation, extra, *args, **kwargs):
        self.extra = extra
        self.settings = get_project_settings()
        self.aws_access_key = self.settings.get('AWS_ACCESS_KEY_ID')
        self.aws_secret_key = self.settings.get('AWS_SECRET_ACCESS_KEY')
        self.aws_associate_tag = self.settings.get('AWS_ASSOCIATE_TAG')
        if not self.aws_access_key:
            raise CloseSpider('`AWS_ACCESS_KEY_ID` is undefined in settings.py.')
        if not self.aws_secret_key:
            raise CloseSpider('`AWS_SECRET_ACCESS_KEY` is undefined in settings.py.')
        self.aws_marketplace = self.settings.get('AWS_MARKETPLACE')
        url = self.make_url(operation, extra)
        kwargs.update({'url': url})
        super(AwsRequest, self).__init__(*args, **kwargs)

    def generate_signature(self, url_params):
        canonical_string = '&'.join(sorted(url_params.split('&')))
        string_to_sign = "GET\n{endpoint}\n/onca/xml\n{params}".format(endpoint=self.aws_marketplace,
                                                                       params=canonical_string)
        signature = base64.b64encode(
            hmac.new(
                bytes(self.aws_secret_key, encoding='ascii'),
                bytes(string_to_sign, encoding='ascii'),
                hashlib.sha256
            ).digest()
        )
        encoded_signature = parse.quote(signature)
        return encoded_signature

    def make_url(self, operation, extra=None):
        extra = extra or {}
        base_params = dict(
            AssociateTag=self.aws_associate_tag,
            AWSAccessKeyId=self.aws_access_key,
            Operation=operation,
            Service='AWSECommerceService',
            Timestamp=formatted_amazon_datetime_str()
        )
        base_params.update(extra)

        # Sort and urlencode the params in accordance to the docs.
        url_params = '&'.join(sorted(urlencode(base_params).split('&')))
        signature = self.generate_signature(url_params)

        # Add the signature to the request url
        url_params += '&Signature={}'.format(signature)
        url = parse.urlunsplit(
            (
                'http',
                self.aws_marketplace,
                '/onca/xml',
                url_params,
                None
            )
        )
        return url


class AwsAsinSearchRequest(AwsRequest):
    OPERATION = 'ItemSearch'

    def __init__(self, search_index, brand, item_page=1, response_groups=('ItemIds', 'Large', 'SearchBins'), extra=None,
                 *args, **kwargs):
        """

        :param search_index: 
        :param brand: 
        :param item_page: 
        :param response_groups: 
        :param args: scrapy Request args. 
        :param kwargs: scrapy Request kwargs.
        """
        self.search_index = search_index
        self.brand = brand
        self.item_page = item_page
        self.response_groups = response_groups
        self.extra = extra
        ex_params = extra or {}
        extra = dict(
            SearchIndex=search_index,
            ResponseGroup=','.join(response_groups),
            Brand=brand,
            Keywords=brand,
            ItemPage=item_page
        )
        extra.update(ex_params)
        super(AwsAsinSearchRequest, self).__init__(self.OPERATION, extra, **kwargs)

    def replace(self, *args, **kwargs):
        """Create a new Request with the same attributes except for those
        given new values.
        """
        for x in ['url', 'method', 'headers', 'body', 'cookies', 'meta',
                  'encoding', 'priority', 'dont_filter', 'callback', 'errback',
                  'search_index', 'brand', 'item_page', 'response_groups', 'extra']:
            kwargs.setdefault(x, getattr(self, x))
        cls = kwargs.pop('cls', self.__class__)
        return cls(*args, **kwargs)