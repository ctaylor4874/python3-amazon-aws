from unittest import TestCase

from aws.parsers.base import Item, Image, ImageSet


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


class TestItemImages(TestCase):
    """
    Test case for item element when images are returned.
    """

    body = """
    <Item xmlns="http://webservices.amazon.com/AWSECommerceService/2011-08-01">
        <ASIN>B005BPZFAO</ASIN>
        <SalesRank>3064</SalesRank>
        <SmallImage>
            <URL>https://images-na.ssl-images-amazon.com/images/I/41mrgRmG5JL._SL75_.jpg</URL>
            <Height Units="pixels">75</Height>
            <Width Units="pixels">67</Width>
        </SmallImage>
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
    </Item>
    """

    def setUp(self):
        self.parser = Item.from_string(self.body)

    def test_asin(self):
        self.assertEqual(self.parser.asin, 'B005BPZFAO')

    def test_sales_rank(self):
        self.assertEqual(self.parser.sales_rank, '3064')

    def test_small_image(self):
        self.assertIsNotNone(self.parser.small_image)
        self.assertIsInstance(self.parser.small_image, Image)

    def test_medium_image(self):
        self.assertIsNotNone(self.parser.medium_image)
        self.assertIsInstance(self.parser.medium_image, Image)

    def test_large_image(self):
        self.assertIsNotNone(self.parser.large_image)
        self.assertIsInstance(self.parser.large_image, Image)


class TestItemImageSets(TestCase):

    body = """
    <Item xmlns="http://webservices.amazon.com/AWSECommerceService/2011-08-01">
        <!-- More stuff excluded -->
        <ImageSets>
            <ImageSet Category="variant">
                <SwatchImage>
                    <URL>https://images-na.ssl-images-amazon.com/images/I/51Etx6EURUL._SL30_.jpg</URL>
                    <Height Units="pixels">21</Height>
                    <Width Units="pixels">30</Width>
                </SwatchImage>
                <SmallImage>
                    <URL>https://images-na.ssl-images-amazon.com/images/I/51Etx6EURUL._SL75_.jpg</URL>
                    <Height Units="pixels">53</Height>
                    <Width Units="pixels">75</Width>
                </SmallImage>
                <ThumbnailImage>
                    <URL>https://images-na.ssl-images-amazon.com/images/I/51Etx6EURUL._SL75_.jpg</URL>
                    <Height Units="pixels">53</Height>
                    <Width Units="pixels">75</Width>
                </ThumbnailImage>
                <TinyImage>
                    <URL>https://images-na.ssl-images-amazon.com/images/I/51Etx6EURUL._SL110_.jpg</URL>
                    <Height Units="pixels">78</Height>
                    <Width Units="pixels">110</Width>
                </TinyImage>
                <MediumImage>
                    <URL>https://images-na.ssl-images-amazon.com/images/I/51Etx6EURUL._SL160_.jpg</URL>
                    <Height Units="pixels">113</Height>
                    <Width Units="pixels">160</Width>
                </MediumImage>
                <LargeImage>
                    <URL>https://images-na.ssl-images-amazon.com/images/I/51Etx6EURUL.jpg</URL>
                    <Height Units="pixels">353</Height>
                    <Width Units="pixels">500</Width>
                </LargeImage>
            </ImageSet>
            <ImageSet Category="primary">
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
        </ImageSets>
    </Item>
    """

    def setUp(self):
        self.parser = Item.from_string(self.body)

    def test_image_set_primary(self):
        img_set = self.parser.image_set_primary
        self.assertIsNotNone(img_set.element)
        self.assertIsInstance(img_set, ImageSet)
        self.assertIsInstance(img_set.swatch_image, Image)
        self.assertEqual(img_set.swatch_image.url, 'https://images-na.ssl-images-amazon.com/images/I/41mrgRmG5JL._SL30_.jpg')

    def test_image_set_variant(self):
        img_set = self.parser.image_set_variant
        self.assertIsNotNone(img_set.element)
        self.assertIsInstance(img_set, ImageSet)
        self.assertIsInstance(img_set.swatch_image, Image)
        self.assertEqual(img_set.swatch_image.url, 'https://images-na.ssl-images-amazon.com/images/I/51Etx6EURUL._SL30_.jpg')
