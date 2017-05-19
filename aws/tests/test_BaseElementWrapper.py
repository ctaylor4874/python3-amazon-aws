from unittest import TestCase

from aws.parsers.base import BaseElementWrapper
from aws.parsers.helpers import parse_bool


class TestBaseElementWrapper(TestCase):

    def test_with_no_element(self):
        parser = BaseElementWrapper(None)
        self.assertFalse(parser)
        self.assertIsNone(parser.xpath('./NoElement'))

    def test_with_element(self):
        # xmlns used to suppress warnings from BaseElementWrapper when no namespace is supplied
        xml_string = '<Element xmlns="suppressWarnings">Testing</Element>'
        parser = BaseElementWrapper.from_string(xml_string)
        self.assertTrue(parser)
        self.assertIsNotNone(parser.xpath('./text()'))
        self.assertEqual(parser.to_string(), xml_string)


class TestParseBool(TestCase):

    def test_true_with_upper(self):
        self.assertTrue(parse_bool(lambda: 'True')())

    def test_true_with_lower(self):
        self.assertTrue(parse_bool(lambda: 'true')())

    def test_false_with_upper(self):
        self.assertFalse(parse_bool(lambda: 'False')())

    def test_false_with_lower(self):
        self.assertFalse(parse_bool(lambda: 'false')())
