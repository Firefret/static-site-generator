from htmlnode import *
import unittest

class TestHtmlNode(unittest.TestCase):
    def test_props_to_html(self):
        html_node = HTMLNode("div", "Hello World", [], {"class": "test"})
        with self.subTest("props present"):
            self.assertEqual(html_node.props_to_html(), ' class="test"')

        html_node.props = {}

        with self.subTest("props empty"):
            self.assertEqual(html_node.props_to_html(), "")

        html_node.props = None
        with self.subTest("props none"):
            self.assertEqual(html_node.props_to_html(), "")

        html_node.props = {"disabled":""}

        with self.subTest("boolean prop"):
            self.assertEqual(html_node.props_to_html(), ' disabled')

        html_node.props = {"disabled":None}
        with self.subTest("boolean prop with None value"):
            self.assertEqual(html_node.props_to_html(), " disabled")