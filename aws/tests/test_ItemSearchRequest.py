from unittest import TestCase

from aws.parsers.base import ItemSearchRequest


class TestItemSearchRequest(TestCase):

    body = """
    <ItemSearchRequest xmlns="http://webservices.amazon.com/AWSECommerceService/2011-08-01">
        <Brand>brand</Brand>
        <ItemPage>2</ItemPage>
        <ResponseGroup>ItemIds</ResponseGroup>
        <SearchIndex>Automotive</SearchIndex>
    </ItemSearchRequest>
    """

    def setUp(self):
        self.parser = ItemSearchRequest.from_string(self.body)

    def test_brand(self):
        self.assertEqual(self.parser.brand, 'brand')

    def test_item_page(self):
        self.assertEqual(self.parser.item_page, '2')

    def test_response_group(self):
        self.assertEqual(len(self.parser.response_groups), 1)
        self.assertEqual(self.parser.response_groups[0], 'ItemIds')

    def test_search_index(self):
        self.assertEqual(self.parser.search_index, 'Automotive')


class TestItemSearchRequestMultipleResponseGroups(TestCase):

    body = """
    <ItemSearchRequest xmlns="http://webservices.amazon.com/AWSECommerceService/2011-08-01">
        <Brand>brand</Brand>
        <ItemPage>1</ItemPage>
        <ResponseGroup>ItemAttributes</ResponseGroup>
        <ResponseGroup>ItemIds</ResponseGroup>
        <ResponseGroup>SearchBins</ResponseGroup>
        <SearchIndex>Automotive</SearchIndex>
    </ItemSearchRequest>
    """

    def setUp(self):
        self.parser = ItemSearchRequest.from_string(self.body)

    def test_brand(self):
        self.assertEqual(self.parser.brand, 'brand')

    def test_item_page(self):
        self.assertEqual(self.parser.item_page, '1')

    def test_response_group(self):
        self.assertEqual(len(self.parser.response_groups), 3)
        self.assertIn('ItemAttributes', self.parser.response_groups)
        self.assertIn('ItemIds', self.parser.response_groups)
        self.assertIn('SearchBins', self.parser.response_groups)

    def test_search_index(self):
        self.assertEqual(self.parser.search_index, 'Automotive')
