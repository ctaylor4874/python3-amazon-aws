import unittest

from aws.parsers.base import Image


class TestImage(unittest.TestCase):

    body = """
    <SmallImage xmlns="http://webservices.amazon.com/AWSECommerceService/2011-08-01">
        <URL>https://images-na.ssl-images-amazon.com/images/I/41mrgRmG5JL._SL75_.jpg</URL>
        <Height Units="pixels">75</Height>
        <Width Units="pixels">67</Width>
    </SmallImage>
    """

    def setUp(self):
        self.parser = Image.from_string(self.body)

    def test_url(self):
        self.assertEqual(self.parser.url, 'https://images-na.ssl-images-amazon.com/images/I/41mrgRmG5JL._SL75_.jpg')

    def test_height(self):
        self.assertEqual(self.parser.height, '75')

    def test_width(self):
        self.assertEqual(self.parser.width, '67')
