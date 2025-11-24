from htmlnode import *
from textnode import *
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


class TestParentNode(unittest.TestCase):
    def test_to_html(self):
        with self.subTest("empty children"):
            self.assertRaises(ValueError, ParentNode("div", []).to_html)

        with self.subTest("one child"):
            child = LeafNode("p", "Hello, world!")
            parent = ParentNode("div", [child])
            self.assertEqual(parent.to_html(), "<div><p>Hello, world!</p></div>")

        with self.subTest("multiple children"):
            child1 = LeafNode("p", "Hello, world!")
            child2 = LeafNode("span", "Balls", )
            parent = ParentNode("div", [child1, child2])
            self.assertEqual(parent.to_html(), "<div><p>Hello, world!</p><span>Balls</span></div>")

        with self.subTest("nested children"):
            child1 = LeafNode("p", "Hello, world!")
            child2 = LeafNode("span", "Balls", {"class": "test"})
            child3 = LeafNode("img", "Image", {"src":"https://firefret.xyz/cocks.jpg"})
            parent = ParentNode("div", [child1, child2], {"disabled": None})
            grandparent = ParentNode("section", [parent, child3])
            self.assertEqual(grandparent.to_html(), "<section><div disabled><p>Hello, world!</p><span class=\"test\">Balls</span></div><img src=\"https://firefret.xyz/cocks.jpg\">Image</img></section>")

class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text_node_to_html_node(self):
        with self.subTest("invalid text type"):
            self.assertRaises(TypeError, text_node_to_html_node(TextNode("Hello, world!", "italic")))

        with self.subTest("plain text"):
            node = TextNode("Hello, world!", TextType.PLAIN)
            node2 = TextNode("Hello, world2!", TextType.TEXT)
            html_node = LeafNode(None, "Hello, world!")
            html_node2 = LeafNode(None, "Hello, world2!")
            self.assertEqual(text_node_to_html_node(node), html_node)
            self.assertEqual(text_node_to_html_node(node2), html_node2)

        with self.subTest("bold text"):
            node = TextNode("Hello, world!", TextType.BOLD)
            html_node = LeafNode("b", "Hello, world!")
            self.assertEqual(text_node_to_html_node(node), html_node)

        with self.subTest("italic text"):
            node = TextNode("Hello, world!", TextType.ITALIC)
            html_node = LeafNode("i", "Hello, world!")
            self.assertEqual(text_node_to_html_node(node), html_node)

        with self.subTest("code text"):
            node = TextNode("Hello, world!", TextType.CODE)
            html_node = LeafNode("code", "Hello, world!")
            self.assertEqual(text_node_to_html_node(node), html_node)

        with self.subTest("link text"):
            node = TextNode("Hello, world!", TextType.LINK, "https://google.com")
            html_node = LeafNode("a", "Hello, world!", {"href": "https://google.com"})
            self.assertEqual(text_node_to_html_node(node), html_node)

        with self.subTest("image text"):
            node = TextNode("Hello, world!", TextType.IMAGE, "https://google.com/image.png")
            html_node = LeafNode("img", "", {"src": "https://google.com/image.png", "alt": "Hello, world!"})
            self.assertEqual(text_node_to_html_node(node), html_node)
