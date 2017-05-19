from unittest import TestCase

from aws.parsers.base import Offer, CurrencyElement


class TestOfferListing(TestCase):

    body = """
    <Offer xmlns="http://webservices.amazon.com/AWSECommerceService/2011-08-01">
        <OfferAttributes>
            <Condition>New</Condition>
        </OfferAttributes>
        <OfferListing>
            <OfferListingId>
                6gcK8m0TkLRj%2BLDlk9bNrVKLeF2jn%2BCGO2iSRt9eT4xgCE6SsqDaZi5fcnZOQrPa4H%2FY8LTMNgkX7nfOkDoT3rWbdksMWEZp9gX0AQ6n0twKTFxJ0cXwTg%3D%3D
            </OfferListingId>
            <Price>
                <Amount>28895</Amount>
                <CurrencyCode>USD</CurrencyCode>
                <FormattedPrice>$288.95</FormattedPrice>
            </Price>
            <Availability>Usually ships in 24 hours</Availability>
            <AvailabilityAttributes>
                <AvailabilityType>now</AvailabilityType>
                <MinimumHours>0</MinimumHours>
                <MaximumHours>0</MaximumHours>
            </AvailabilityAttributes>
            <IsEligibleForSuperSaverShipping>1</IsEligibleForSuperSaverShipping>
            <IsEligibleForPrime>1</IsEligibleForPrime>
        </OfferListing>
    </Offer>
    """

    def setUp(self):
        self.parser = Offer.from_string(self.body)

    def test_merchant_name(self):
        self.assertIsNone(self.parser.merchant)

    def test_offer_condition(self):
        self.assertEqual(self.parser.condition, 'New')

    def test_price(self):
        self.assertIsInstance(self.parser.price, CurrencyElement)
        self.assertTrue(self.parser.price)
        self.assertEqual(self.parser.price.amount, '28895')
        self.assertEqual(self.parser.price.currency_code, 'USD')
        self.assertEqual(self.parser.price.formatted_price, '$288.95')

    def test_amount_saved(self):
        self.assertIsInstance(self.parser.amount_saved, CurrencyElement)
        self.assertFalse(self.parser.amount_saved)
        self.assertIsNone(self.parser.amount_saved.amount)
        self.assertIsNone(self.parser.amount_saved.currency_code)
        self.assertIsNone(self.parser.amount_saved.formatted_price)

    def test_availability(self):
        self.assertEqual(self.parser.availability, 'Usually ships in 24 hours')