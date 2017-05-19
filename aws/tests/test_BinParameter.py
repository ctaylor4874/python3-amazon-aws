from unittest import TestCase

from aws.parsers.base import BinParameter


class TestBinParameter(TestCase):

    body = """
    <BinParameter xmlns="http://webservices.amazon.com/AWSECommerceService/2011-08-01">
        <Name>Brand</Name>
        <Value>Brand Name</Value>
    </BinParameter>
    """

    def setUp(self):
        self.parser = BinParameter.from_string(self.body)

    def test_name(self):
        self.assertEqual(self.parser.name, 'Brand')

    def test_value(self):
        self.assertEqual(self.parser.value, 'Brand Name')
