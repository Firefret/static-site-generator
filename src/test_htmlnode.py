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

class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        node = LeafNode("p", "Hello, world!")
        with self.subTest("normal node"):
            self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

        node = LeafNode("p", None)
        with self.subTest("None value"):
            self.assertRaises(ValueError, node.to_html)

        node = LeafNode("p", "")
        with self.subTest("Empty value"):
            self.assertRaises(ValueError, node.to_html)

        node = LeafNode(None, "Hello, world!")
        with self.subTest("None tag"):
            self.assertEqual(node.to_html(), "Hello, world!")

        node = LeafNode("", "Hello, world!")
        with self.subTest("Empty tag"):
            self.assertEqual(node.to_html(), "Hello, world!")

        node = LeafNode("p", "Hello, world!", {"class": "test"})
        with self.subTest("props"):
            self.assertEqual(node.to_html(), "<p class=\"test\">Hello, world!</p>")

        node = LeafNode("p", "Hello, world!", {"disabled": None})
        with self.subTest("props with None value"):
            self.assertEqual(node.to_html(), "<p disabled>Hello, world!</p>")
