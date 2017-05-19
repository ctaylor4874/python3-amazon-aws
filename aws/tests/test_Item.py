from unittest import TestCase

from aws.parsers.base import Item


class TestItem(TestCase):
    """
    Testcase for item element when only ItemIds is requested.
    """

    body = """
    <Item xmlns="http://webservices.amazon.com/AWSECommerceService/2011-08-01">
        <ASIN>asin</ASIN>
    </Item>
    """

    def setUp(self):
        self.parser = Item.from_string(self.body)
        """:type parser: Item"""

    def test_asin(self):
        self.assertEqual(self.parser.asin, 'asin')

    def test_sales_rank(self):
        self.assertIsNone(self.parser.sales_rank)


class TestItemSalesRank(TestCase):
    """
        Testcase for item element when only ItemIds&|SalesRank is requested.
        """

    body = """
        <Item xmlns="http://webservices.amazon.com/AWSECommerceService/2011-08-01">
            <ASIN>asin</ASIN>
            <SalesRank>100</SalesRank>
        </Item>
        """

    def setUp(self):
        self.parser = Item.from_string(self.body)
        """:type parser: Item"""

    def test_asin(self):
        self.assertEqual(self.parser.asin, 'asin')

    def test_sales_rank(self):
        self.assertEqual(self.parser.sales_rank, '100')
