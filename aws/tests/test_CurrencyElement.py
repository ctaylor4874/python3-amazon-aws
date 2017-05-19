from unittest import TestCase

from aws.parsers.base import CurrencyElement, ITEM_SEARCH_NAMESPACES


class TestCurrencyElement(TestCase):

    body = """
    <LowestNewPrice xmlns="http://webservices.amazon.com/AWSECommerceService/2011-08-01">
        <Amount>28895</Amount>
        <CurrencyCode>USD</CurrencyCode>
        <FormattedPrice>$288.95</FormattedPrice>
    </LowestNewPrice>
    """

    def setUp(self):
        self.parser = CurrencyElement.from_string(self.body, namespaces=ITEM_SEARCH_NAMESPACES)

    def test_amount(self):
        self.assertEqual(self.parser.amount, '28895')

    def test_currency_code(self):
        self.assertEqual(self.parser.currency_code, 'USD')

    def test_formatted_price(self):
        self.assertEqual(self.parser.formatted_price, '$288.95')
