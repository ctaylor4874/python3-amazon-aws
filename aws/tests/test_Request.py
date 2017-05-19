from unittest import TestCase

from aws.parsers.base import ErrorElement
from aws.parsers.base import Request, ItemSearchRequest


class TestValidRequest(TestCase):

    body = """
    <Request xmlns="http://webservices.amazon.com/AWSECommerceService/2011-08-01">
        <IsValid>True</IsValid>
        <ItemSearchRequest></ItemSearchRequest>
    </Request>
    """

    def setUp(self):
        self.parser = Request.from_string(self.body)

    def test_is_valid(self):
        self.assertTrue(self.parser.is_valid)

    def test_item_search_request(self):
        self.assertTrue(self.parser.item_search_request)
        self.assertIsInstance(self.parser.item_search_request, ItemSearchRequest)

    def test_errors(self):
        self.assertEqual(len(self.parser.errors), 0)

class TestInvalidRequest(TestCase):

    body = """
    <Request xmlns="http://webservices.amazon.com/AWSECommerceService/2011-08-01">
        <IsValid>False</IsValid>
        <ItemSearchRequest></ItemSearchRequest>
    </Request>
    """

    def setUp(self):
        self.parser = Request.from_string(self.body)

    def test_is_valid(self):
        self.assertFalse(self.parser.is_valid)

    def test_item_search_request(self):
        self.assertTrue(self.parser.item_search_request)
        self.assertIsInstance(self.parser.item_search_request, ItemSearchRequest)

    def test_errors(self):
        self.assertEqual(len(self.parser.errors), 0)

class TestErrorRequest(TestCase):

    body = """
    <Request xmlns="http://webservices.amazon.com/AWSECommerceService/2011-08-01">
        <IsValid>True</IsValid>
        <ItemSearchRequest></ItemSearchRequest>
        <Errors>
            <Error>
                <Code>AWS.ECommerceService.NoExactMatches</Code>
                <Message>We did not find any matches for your request.</Message>
            </Error>
        </Errors>
    </Request>
    """

    def setUp(self):
        self.parser = Request.from_string(self.body)

    def test_is_valid(self):
        self.assertTrue(self.parser.is_valid)

    def test_item_search_request(self):
        self.assertTrue(self.parser.item_search_request)
        self.assertIsInstance(self.parser.item_search_request, ItemSearchRequest)

    def test_errors(self):
        self.assertEqual(len(self.parser.errors), 1)
        self.assertIsInstance(self.parser.errors[0], ErrorElement)
