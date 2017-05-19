from unittest import TestCase

from aws.parsers.base import Bin, BinParameter


class TestBin(TestCase):

    body = """
    <Bin xmlns="http://webservices.amazon.com/AWSECommerceService/2011-08-01">
        <BinName>Bin Name</BinName>
        <BinItemCount>1</BinItemCount>
        <BinParameter></BinParameter>
    </Bin>
    """

    def setUp(self):
        self.parser = Bin.from_string(self.body)

    def test_bin_name(self):
        self.assertEqual(self.parser.bin_name, 'Bin Name')

    def test_bin_item_count(self):
        self.assertEqual(self.parser.bin_item_count, '1')

    def test_bin_parameter(self):
        self.assertTrue(self.parser.bin_parameter)
        self.assertIsInstance(self.parser.bin_parameter, BinParameter)
