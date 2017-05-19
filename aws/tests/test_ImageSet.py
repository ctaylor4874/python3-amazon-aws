import unittest

from aws.parsers.base import ImageSet, Image


class TestImageSet(unittest.TestCase):

    body = """
    <ImageSet Category="primary" xmlns="http://webservices.amazon.com/AWSECommerceService/2011-08-01">
        <SwatchImage>
            <URL>https://images-na.ssl-images-amazon.com/images/I/41mrgRmG5JL._SL30_.jpg</URL>
            <Height Units="pixels">30</Height>
            <Width Units="pixels">27</Width>
        </SwatchImage>
        <SmallImage>
            <URL>https://images-na.ssl-images-amazon.com/images/I/41mrgRmG5JL._SL75_.jpg</URL>
            <Height Units="pixels">75</Height>
            <Width Units="pixels">67</Width>
        </SmallImage>
        <ThumbnailImage>
            <URL>https://images-na.ssl-images-amazon.com/images/I/41mrgRmG5JL._SL75_.jpg</URL>
            <Height Units="pixels">75</Height>
            <Width Units="pixels">67</Width>
        </ThumbnailImage>
        <TinyImage>
            <URL>https://images-na.ssl-images-amazon.com/images/I/41mrgRmG5JL._SL110_.jpg</URL>
            <Height Units="pixels">110</Height>
            <Width Units="pixels">99</Width>
        </TinyImage>
        <MediumImage>
            <URL>https://images-na.ssl-images-amazon.com/images/I/41mrgRmG5JL._SL160_.jpg</URL>
            <Height Units="pixels">160</Height>
            <Width Units="pixels">143</Width>
        </MediumImage>
        <LargeImage>
            <URL>https://images-na.ssl-images-amazon.com/images/I/41mrgRmG5JL.jpg</URL>
            <Height Units="pixels">500</Height>
            <Width Units="pixels">448</Width>
        </LargeImage>
    </ImageSet>
    """

    def setUp(self):
        self.parser = ImageSet.from_string(self.body)

    def test_swatch_image(self):
        img = self.parser.swatch_image
        self.assertIsInstance(img, Image)
        self.assertIsNotNone(img.element)

    def test_small_image(self):
        img = self.parser.small_image
        self.assertIsInstance(img, Image)
        self.assertIsNotNone(img.element)

    def test_thumbnail_image(self):
        img = self.parser.thumbnail_image
        self.assertIsInstance(img, Image)
        self.assertIsNotNone(img.element)

    def test_tiny_image(self):
        img = self.parser.tiny_image
        self.assertIsInstance(img, Image)
        self.assertIsNotNone(img.element)

    def test_medium_image(self):
        img = self.parser.medium_image
        self.assertIsInstance(img, Image)
        self.assertIsNotNone(img.element)

    def test_large_image(self):
        img = self.parser.large_image
        self.assertIsInstance(img, Image)
        self.assertIsNotNone(img.element)
