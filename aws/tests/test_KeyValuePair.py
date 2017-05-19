from unittest import TestCase
from aws.parsers.base import KeyValuePair

class TestKeyValuePair(TestCase):

    body = """
    <AnyKeyValuePairElement xmlns="http://webservices.amazon.com/AWSECommerceService/2011-08-01" 
        Name="UserAgent" 
        Value="my-user-agent">
    </AnyKeyValuePairElement>
    """

    def setUp(self):
        self.parser = KeyValuePair.from_string(self.body)

    def test_name(self):
        self.assertEqual(self.parser.name, 'UserAgent')

    def test_value(self):
        self.assertEqual(self.parser.value, 'my-user-agent')

    def test_as_tuple(self):
        self.assertEqual(self.parser.as_tuple(), ('UserAgent', 'my-user-agent'))
