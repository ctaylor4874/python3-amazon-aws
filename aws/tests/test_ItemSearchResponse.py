import unittest

from aws.parsers.base import OperationRequest, Items, Item
from aws.parsers.itemsearch import ItemSearchResponse


class TestItemSearchResponse(unittest.TestCase):

    body = """
    <ItemLookupResponse xmlns="http://webservices.amazon.com/AWSECommerceService/2011-08-01">
        <OperationRequest>
            <HTTPHeaders>
                <Header Name="UserAgent" Value="python-requests/2.13.0"></Header>
            </HTTPHeaders>
            <RequestId>5f1f3c24-59ef-4d77-b6cc-a09544441bcb</RequestId>
            <Arguments>
                <Argument Name="AWSAccessKeyId" Value="asdf"></Argument>
                <Argument Name="AssociateTag" Value="asdf"></Argument>
                <Argument Name="ItemId"
                          Value="B005BPZFAO"></Argument>
                <Argument Name="Operation" Value="ItemLookup"></Argument>
                <Argument Name="ResponseGroup" Value="OfferFull,SalesRank,ItemAttributes,Images"></Argument>
                <Argument Name="Service" Value="AWSECommerceService"></Argument>
                <Argument Name="Timestamp" Value="2017-05-19T20:25:35.000Z"></Argument>
                <Argument Name="Signature" Value="asdf"></Argument>
            </Arguments>
            <RequestProcessingTime>0.0656455190000000</RequestProcessingTime>
        </OperationRequest>
        <Items>
            <Request>
                <IsValid>True</IsValid>
                <ItemLookupRequest>
                    <IdType>ASIN</IdType>
                    <ItemId>B005BPZFAO</ItemId>
                    <ResponseGroup>OfferFull</ResponseGroup>
                    <ResponseGroup>SalesRank</ResponseGroup>
                    <ResponseGroup>ItemAttributes</ResponseGroup>
                    <ResponseGroup>Images</ResponseGroup>
                    <VariationPage>All</VariationPage>
                </ItemLookupRequest>
            </Request>
            <Item>
                <ASIN>B005BPZFAO</ASIN>
            </Item>
        </Items>
    </ItemLookupResponse>
    """

    def setUp(self):
        self.parser = ItemSearchResponse.from_string(self.body)

    def test_operation_request(self):
        self.assertIsInstance(self.parser.operation_request, OperationRequest)
        self.assertEqual(self.parser.operation_request.request_id, '5f1f3c24-59ef-4d77-b6cc-a09544441bcb')

    def test_items(self):
        self.assertIsInstance(self.parser.items, Items)
        self.assertEqual(len(self.parser.items.items), 1)
        self.assertIsInstance(self.parser.items.items[0], Item)
        self.assertEqual(self.parser.items.items[0].asin, 'B005BPZFAO')
