from unittest import TestCase

from aws.parsers.base import OfferSummary, CurrencyElement


class TestOfferSummary(TestCase):

    body = """
    <OfferSummary xmlns="http://webservices.amazon.com/AWSECommerceService/2011-08-01">
        <LowestNewPrice>
            <Amount>28895</Amount>
            <CurrencyCode>USD</CurrencyCode>
            <FormattedPrice>$288.95</FormattedPrice>
        </LowestNewPrice>
        <LowestUsedPrice>
            <Amount>19681</Amount>
            <CurrencyCode>USD</CurrencyCode>
            <FormattedPrice>$196.81</FormattedPrice>
        </LowestUsedPrice>
        <TotalNew>33</TotalNew>
        <TotalUsed>4</TotalUsed>
        <TotalCollectible>0</TotalCollectible>
        <TotalRefurbished>0</TotalRefurbished>
    </OfferSummary>
    """

    def setUp(self):
        self.parser = OfferSummary.from_string(self.body)

    def test_lowest_new_price(self):
        self.assertIsInstance(self.parser.lowest_new_price, CurrencyElement)
        self.assertEqual(self.parser.lowest_new_price.amount, '28895')
        self.assertEqual(self.parser.lowest_new_price.currency_code, 'USD')
        self.assertEqual(self.parser.lowest_new_price.formatted_price, '$288.95')

    def test_lowest_used_price(self):
        self.assertIsInstance(self.parser.lowest_used_price, CurrencyElement)
        self.assertEqual(self.parser.lowest_used_price.amount, '19681')
        self.assertEqual(self.parser.lowest_used_price.currency_code, 'USD')
        self.assertEqual(self.parser.lowest_used_price.formatted_price, '$196.81')

    def test_total_new(self):
        self.assertEqual(self.parser.total_new, '33')

    def test_total_used(self):
        self.assertEqual(self.parser.total_used, '4')

    def test_total_collectible(self):
        self.assertEqual(self.parser.total_collectible, '0')

    def test_total_refurbished(self):
        self.assertEqual(self.parser.total_refurbished, '0')
