from unittest import TestCase

from aws.parsers.base import OperationRequest


class TestOperationRequest(TestCase):

    body = """
    <OperationRequest xmlns="http://webservices.amazon.com/AWSECommerceService/2011-08-01">
        <HTTPHeaders>
            <Header></Header>
        </HTTPHeaders>
        <RequestId>request-id</RequestId>
        <Arguments>
            <Argument Name="AWSAccessKeyId" Value="aws-access-key"></Argument>
            <Argument Name="AssociateTag" Value="associate-tag"></Argument>
            <Argument Name="Brand" Value="brand"></Argument>
            <Argument Name="ItemPage" Value="1"></Argument>
            <Argument Name="Operation" Value="ItemSearch"></Argument>
            <Argument Name="ResponseGroup" Value="ItemIds"></Argument>
            <Argument Name="SearchIndex" Value="Automotive"></Argument>
            <Argument Name="Service" Value="AWSECommerceService"></Argument>
            <Argument Name="Timestamp" Value="2017-05-01T17:03:27.000Z"></Argument>
            <Argument Name="Signature" Value="signature"></Argument>
        </Arguments>
        <RequestProcessingTime>0.123</RequestProcessingTime>
    </OperationRequest>
    """

    def setUp(self):
        self.parser = OperationRequest.from_string(self.body)

    def test_headers(self):
        self.assertEqual(len(self.parser.http_headers), 1)

    def test_request_id(self):
        self.assertEqual(self.parser.request_id, 'request-id')

    def test_arguments(self):
        self.assertEqual(len(self.parser.arguments), 10)

    def test_request_processing_time(self):
        self.assertEqual(self.parser.request_processing_time, '0.123')
