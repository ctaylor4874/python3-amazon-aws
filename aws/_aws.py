import base64
import sys
import datetime
import hashlib
from urllib import parse
import hmac
import os


MARKETPLACES = {
    'us': 'webservices.amazon.com',
    'br': 'webservices.amazon.com.br',
    'ca': 'webservices.amazon.ca',
    'cn': 'webservices.amazon.cn',
    'de': 'webservices.amazon.de',
    'es': 'webservices.amazon.es',
    'fr': 'webservices.amazon.fr',
    'in': 'webservices.amazon.in',
    'it': 'webservices.amazon.it',
    'jp': 'webservices.amazon.jp',
    'mx': 'webservices.amazon.com.mx',
    'uk': 'webservices.amazon.co.uk'
}


def convert_to_gmtime(dt):
    """
    Convert the supplied date to GMT.
    :param dt:
    :return: parameter converted to GMT.
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


class AWS(object):
    version = ''

    def __init__(self, associate_tag, access_key, secret_key, marketplace=None):
        """

        :param associate_tag: An alphanumeric token that uniquely identifies you as an Associate.
        :param access_key: Your AWS Access Key ID which uniquely identifies you.
        :param secret_key: A key that is used in conjunction with the Access Key ID
            to cryptographically sign an API request.
        :param marketplace: The locale where you are making the request.
        """
        import requests
        self.associate_tag = associate_tag
        self.access_key = access_key
        self.secret_key = secret_key
        self.marketplace = marketplace or MARKETPLACES['us']
        self.session = requests.Session()
        self.session.headers['User-Agent'] = 'python-amazon-aws'

    def generate_signature(self, url_params):
        canonical_string = '&'.join(sorted(url_params.split('&')))
        string_to_sign = "GET\n{endpoint}\n/onca/xml\n{params}".format(endpoint=self.marketplace,
                                                                       params=canonical_string)
        signature = base64.b64encode(
            hmac.new(bytes(self.secret_key, encoding='ascii'), bytes(string_to_sign, encoding='ascii'),
                     hashlib.sha256).digest())
        encoded_signature = parse.quote(signature)
        return encoded_signature

    def make_request(self, operation, extra=None):
        """

        :param operation: Specifies the Product Advertising API operation to execute. For more information, see Operations.
            http://docs.aws.amazon.com/AWSECommerceService/latest/DG/CHAP_OperationListAlphabetical.html
        :param extra: Any extra parameters which are required for a specific operation.
        :return: AWS API Response content. Default XML String.
        """
        extra = extra or {}
        base_params = dict(
            AssociateTag=self.associate_tag,
            AWSAccessKeyId=self.access_key,
            Operation=operation,
            Service='AWSECommerceService',
            Timestamp=formatted_amazon_datetime_str()
        )
        base_params.update(extra)
        url_params = '&'.join(sorted(urlencode(base_params).split('&')))
        signature = self.generate_signature(url_params)
        url_params += '&Signature=%s' % signature
        url = parse.urlunsplit((
            'http',
            self.marketplace,
            '/onca/xml',
            url_params,
            None
        ))
        response = self.session.get(url)
        content = response.text
        return content


class Search(AWS):
    from aws.parsers.base import raise_error_for_content
    version = '2013-08-01'

    @raise_error_for_content
    def brand_search(self, search_index, brand='', item_page=1, **kwargs):
        extra = dict(
            SearchIndex=search_index,
            ResponseGroup='SearchBins',
            Keywords=brand,
            ItemPage=item_page
        )
        extra.update(kwargs)
        return self.make_request('ItemSearch', extra=extra)

    @raise_error_for_content
    def asin_search(self, search_index, brand, item_page=1, **kwargs):
        """
        Search for asins within a search index for a specified brand.

        :param search_index: Automotive, Electronics, etc.
        :param brand: Brand name or part of a brand name.
        :param item_page: 1-10.
        :param kwargs: Any extra url params to be sent to the api.
        :return: XML Document taken from the response.
        """
        extra = dict(
            SearchIndex=search_index,
            ResponseGroup='ItemIds,Large,SearchBins',
            Brand=brand,
            Keywords=brand,
            # Manufacturer=brand,
            ItemPage=item_page
        )
        extra.update(**kwargs)
        return self.make_request('ItemSearch', extra=extra)


class Lookup(AWS):
    from aws.parsers.base import raise_error_for_content
    version = '2013-08-01'

    @raise_error_for_content
    def item_lookup(self, item_ids=(), response_groups=(), **kwargs):
        """
        http://docs.aws.amazon.com/AWSECommerceService/latest/DG/ItemLookup.html

        :param item_ids:
        """
        extra = {'ItemId': ','.join(item_ids), 'ResponseGroup': ','.join(response_groups)}
        extra.update(kwargs)
        r = self.make_request('ItemLookup', extra=extra)
        return r
