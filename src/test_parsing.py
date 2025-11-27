import unittest
from parsing import *
from textnode import TextNode, TextType


class TestSplitNodesDelimiter(unittest.TestCase):

    def test_split_nodes_delimiter(self):

        # ---------- Invalid or error conditions ----------

        with self.subTest("empty input list"):
            self.assertRaises(ValueError, split_nodes_delimiter, [], " ", TextType.TEXT)

        with self.subTest("empty delimiter string"):
            self.assertRaises(
                ValueError,
                split_nodes_delimiter,
                [TextNode("Hello, world!", TextType.TEXT)],
                "",
                TextType.TEXT
            )

        with self.subTest("delimiter not in allowed list"):
            self.assertRaises(
                ValueError,
                split_nodes_delimiter,
                [TextNode("Hello, world!", TextType.TEXT)],
                "!",
                TextType.TEXT
            )

        with self.subTest("delimiter absent in string"):
            nodes = [TextNode("Hello, world!", TextType.TEXT)]
            self.assertRaises(
                ValueError,
                split_nodes_delimiter,
                nodes,
                "_",
                TextType.ITALIC
            )

        with self.subTest("delimiter lacks matching pair"):
            self.assertRaises(
                ValueError,
                split_nodes_delimiter,
                [TextNode("Hello, _world!", TextType.TEXT)],
                "_",
                TextType.ITALIC
            )


        # ---------- Valid transformations ----------

        with self.subTest("basic valid pair"):
            self.assertEqual(
                split_nodes_delimiter(
                    [TextNode("Hello, _world_!", TextType.TEXT)],
                    "_",
                    TextType.ITALIC
                ),
                [
                    TextNode("Hello, ", TextType.TEXT),
                    TextNode("world", TextType.ITALIC),
                    TextNode("!", TextType.TEXT),
                ]
            )

        with self.subTest("delimiter at beginning"):
            self.assertEqual(
                split_nodes_delimiter(
                    [TextNode("_Hello_, world!", TextType.TEXT)],
                    "_",
                    TextType.ITALIC
                ),
                [
                    TextNode("Hello", TextType.ITALIC),
                    TextNode(", world!", TextType.TEXT),
                ]
            )

        with self.subTest("delimiter at end"):
            self.assertEqual(
                split_nodes_delimiter(
                    [TextNode("Hello _world_", TextType.TEXT)],
                    "_",
                    TextType.ITALIC
                ),
                [
                    TextNode("Hello ", TextType.TEXT),
                    TextNode("world", TextType.ITALIC),
                ]
            )

        with self.subTest("multiple delimiter pairs in one string"):
            self.assertEqual(
                split_nodes_delimiter(
                    [TextNode("A _B_ C _D_ E", TextType.TEXT)],
                    "_",
                    TextType.ITALIC
                ),
                [
                    TextNode("A ", TextType.TEXT),
                    TextNode("B", TextType.ITALIC),
                    TextNode(" C ", TextType.TEXT),
                    TextNode("D", TextType.ITALIC),
                    TextNode(" E", TextType.TEXT),
                ]
            )

        with self.subTest("adjacent delimiters (skip empty items)"):
            # "__Hello__" → splits → ["", "Hello", ""]
            self.assertEqual(
                split_nodes_delimiter(
                    [TextNode("__Hello__", TextType.TEXT)],
                    "_",
                    TextType.ITALIC
                ),
                [
                    TextNode("Hello", TextType.TEXT)
                ]
            )

        with self.subTest("multiple input nodes"):
            nodes = [
                TextNode("Hello _world_!", TextType.TEXT),
                TextNode("This is _cool_!", TextType.TEXT)
            ]
            self.assertEqual(
                split_nodes_delimiter(nodes, "_", TextType.ITALIC),
                [
                    TextNode("Hello ", TextType.TEXT),
                    TextNode("world", TextType.ITALIC),
                    TextNode("!", TextType.TEXT),
                    TextNode("This is ", TextType.TEXT),
                    TextNode("cool", TextType.ITALIC),
                    TextNode("!", TextType.TEXT),
                ]
            )

        with self.subTest("nodes with disallowed types are passed unchanged"):
            nodes = [
                TextNode("Hello _world_!", TextType.TEXT),
                TextNode("IGNORE", TextType.BOLD),  # should be preserved
            ]
            self.assertEqual(
                split_nodes_delimiter(nodes, "_", TextType.ITALIC),
                [
                    TextNode("Hello ", TextType.TEXT),
                    TextNode("world", TextType.ITALIC),
                    TextNode("!", TextType.TEXT),
                    TextNode("IGNORE", TextType.BOLD),
                ]
            )

class TestMarkdownExtraction(unittest.TestCase):

    def test_extract_markdown_images(self):
        cases = [
            (
                "single image",
                "![rick roll](https://i.imgur.com/aKaOqIh.gif)",
                [("rick roll", "https://i.imgur.com/aKaOqIh.gif")],
            ),
            (
                "multiple images",
                "![one](a.png) text ![two](b.jpg)",
                [("one", "a.png"), ("two", "b.jpg")],
            ),
            (
                "no images",
                "this text has no image syntax",
                [],
            ),
            (
                "mixed content with links",
                "![img](x) [link](y) ![pic](z)",
                [("img", "x"), ("pic", "z")],
            ),
            (
                "malformed url allowed",
                "![alt](not a real url)",
                [("alt", "not a real url")],
            ),
        ]

        for label, input_text, expected in cases:
            with self.subTest(label=label):
                self.assertEqual(extract_markdown_images(input_text), expected)

    def test_extract_markdown_links(self):
        cases = [
            (
                "single link",
                "[to youtube](https://www.youtube.com/@bootdotdev)",
                [("to youtube", "https://www.youtube.com/@bootdotdev")],
            ),
            (
                "multiple links",
                "[one](balls.com) text [two](cock.ua)",
                [("one", "balls.com"), ("two", "cock.ua")],
            ),
            (
                "no links",
                "text without markdown links",
                [],
            ),
            (
                "images ignored",
                "![img](x) [link](y) ![pic](z)",
                [("link", "y")],
            ),
            (
                "malformed url allowed",
                "[text](not a real url)",
                [("text", "not a real url")],
            ),
        ]

        for label, input_text, expected in cases:
            with self.subTest(label=label):
                self.assertEqual(extract_markdown_links(input_text), expected)

class TestNodeImageLinkNodeSplit(unittest.TestCase):
    def test_split_nodes_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_nodes_link(self):
        node = TextNode(
            "This is text with a [link](https://www.google.com) and another [second link](https://www.google.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.google.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://www.google.com"),
            ],
            new_nodes,
        )


if __name__ == '__main__':
    unittest.main()
