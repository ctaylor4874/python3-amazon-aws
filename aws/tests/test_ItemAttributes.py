from unittest import TestCase

from aws.parsers.base import ItemAttributes


class TestItemAttributes(TestCase):
    """
    Testcase for item element when only ItemIds is requested.
    """

    body = """
    <ItemAttributes xmlns="http://webservices.amazon.com/AWSECommerceService/2011-08-01">
        <Brand>Magic Chef</Brand>
        <Manufacturer>MC Appliance Corporation</Manufacturer>
        <Title>Magic Chef MCSCD6W3 6 Place Setting Countertop Dishwasher, White</Title>
    </ItemAttributes>
    """

    def setUp(self):
        self.parser = ItemAttributes.from_string(self.body)
        """:type parser: ItemAttributes"""

    def test_brand(self):
        self.assertEqual(self.parser.brand, 'Magic Chef')

    def test_manufacturer(self):
        self.assertEqual(self.parser.manufacturer, 'MC Appliance Corporation')

    def test_title(self):
        self.assertEqual(self.parser.title, 'Magic Chef MCSCD6W3 6 Place Setting Countertop Dishwasher, White')


class TestItemAttributesFullData(TestCase):
    """
    Testcase for item element when only ItemIds is requested.
    """

    body = """
    <ItemAttributes xmlns="http://webservices.amazon.com/AWSECommerceService/2011-08-01">
        <Binding>Misc.</Binding>
        <Brand>Magic Chef</Brand>
        <CatalogNumberList>
            <CatalogNumberListElement>MCSCD6W3 P09036</CatalogNumberListElement>
        </CatalogNumberList>
        <Color>White</Color>
        <EAN>0783761459095</EAN>
        <EANList>
            <EANListElement>0783761459095</EANListElement>
            <EANListElement>0765042454319</EANListElement>
            <EANListElement>0780320076212</EANListElement>
            <EANListElement>0665679014347</EANListElement>
            <EANListElement>0043981790560</EANListElement>
            <EANListElement>0731215390821</EANListElement>
        </EANList>
        <Feature>6 Place Settings, 680 Watts</Feature>
        <Feature>5 Programs with Quick Wash. Stainless Steel Interior</Feature>
        <Feature>Floating Switch Anti-flood Device</Feature>
        <Feature>Detergent and Rinse Aid Dispenser</Feature>
        <Feature>70" Inlet Hose / 47" Outlet hose</Feature>
        <IsAdultProduct>0</IsAdultProduct>
        <ItemDimensions>
            <Height Units="hundredths-inches">1720</Height>
            <Length Units="hundredths-inches">2040</Length>
            <Weight Units="hundredths-pounds">4950</Weight>
            <Width Units="hundredths-inches">2170</Width>
        </ItemDimensions>
        <Label>MC Appliance Corporation</Label>
        <ListPrice>
            <Amount>28895</Amount>
            <CurrencyCode>USD</CurrencyCode>
            <FormattedPrice>$288.95</FormattedPrice>
        </ListPrice>
        <Manufacturer>MC Appliance Corporation</Manufacturer>
        <Model>MCSCD6W3</Model>
        <MPN>MCSCD6W3</MPN>
        <NumberOfItems>1</NumberOfItems>
        <PackageDimensions>
            <Height Units="hundredths-inches">2250</Height>
            <Length Units="hundredths-inches">2550</Length>
            <Weight Units="hundredths-pounds">7400</Weight>
            <Width Units="hundredths-inches">2370</Width>
        </PackageDimensions>
        <PackageQuantity>1</PackageQuantity>
        <PartNumber>MCSCD6W3</PartNumber>
        <ProductGroup>Major Appliances</ProductGroup>
        <ProductTypeName>DISHWASHER</ProductTypeName>
        <Publisher>MC Appliance Corporation</Publisher>
        <Studio>MC Appliance Corporation</Studio>
        <Title>Magic Chef MCSCD6W3 6 Place Setting Countertop Dishwasher, White</Title>
        <UPC>665679014347</UPC>
        <UPCList>
            <UPCListElement>665679014347</UPCListElement>
            <UPCListElement>731215390821</UPCListElement>
            <UPCListElement>780320076212</UPCListElement>
            <UPCListElement>783761459095</UPCListElement>
            <UPCListElement>765042454319</UPCListElement>
            <UPCListElement>043981790560</UPCListElement>
        </UPCList>
        <Warranty>1 year Parts and Labor</Warranty>
    </ItemAttributes>
    """

    def setUp(self):
        self.parser = ItemAttributes.from_string(self.body)
        """:type parser: ItemAttributes"""

    def test_brand(self):
        self.assertEqual(self.parser.brand, 'Magic Chef')

    def test_manufacturer(self):
        self.assertEqual(self.parser.manufacturer, 'MC Appliance Corporation')

    def test_title(self):
        self.assertEqual(self.parser.title, 'Magic Chef MCSCD6W3 6 Place Setting Countertop Dishwasher, White')

    def test_publisher(self):
        self.assertEqual(self.parser.publisher, 'MC Appliance Corporation')

    def test_color(self):
        self.assertEqual(self.parser.color, 'White')

    def test_label(self):
        self.assertEqual(self.parser.label, 'MC Appliance Corporation')
