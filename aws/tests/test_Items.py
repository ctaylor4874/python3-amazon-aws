from unittest import TestCase

from aws.parsers.base import Items, Item


class TestItems(TestCase):
    body = """
    <Items xmlns="http://webservices.amazon.com/AWSECommerceService/2011-08-01">
        <Request></Request>
        <TotalResults>1365</TotalResults>
        <TotalPages>137</TotalPages>
        <MoreSearchResultsUrl>url</MoreSearchResultsUrl>
        <Item></Item>
        <Item></Item>
        <Item></Item>
        <Item></Item>
        <Item></Item>
        <Item></Item>
        <Item></Item>
        <Item></Item>
        <Item></Item>
        <Item></Item>
    </Items>
    """

    def setUp(self):
        self.parser = Items.from_string(self.body)

    def test_request(self):
        self.assertTrue(self.parser.request)

    def test_total_results(self):
        self.assertEqual(self.parser.total_results, '1365')

    def test_total_pages(self):
        self.assertEqual(self.parser.total_pages, '137')

    def test_more_search_results_url(self):
        self.assertEqual(self.parser.more_search_results_url, 'url')

    def test_items(self):
        self.assertEqual(len(self.parser.items), 10)
        self.assertIsInstance(self.parser.items[0], Item)


class TestItemsItemLookup(TestCase):
    body = """
    <Items xmlns="http://webservices.amazon.com/AWSECommerceService/2011-08-01">
        <Request></Request>
        <Item></Item>
        <Item></Item>
        <Item></Item>
        <Item></Item>
        <Item></Item>
        <Item></Item>
        <Item></Item>
        <Item></Item>
        <Item></Item>
        <Item></Item>
    </Items>
    """

    def setUp(self):
        self.parser = Items.from_string(self.body)

    def test_request(self):
        self.assertTrue(self.parser.request)

    def test_total_results(self):
        self.assertIsNone(self.parser.total_results)

    def test_total_pages(self):
        self.assertIsNone(self.parser.total_pages)

    def test_more_search_results_url(self):
        self.assertIsNone(self.parser.more_search_results_url)

    def test_items(self):
        self.assertEqual(len(self.parser.items), 10)
        self.assertIsInstance(self.parser.items[0], Item)
