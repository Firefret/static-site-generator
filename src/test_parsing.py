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


if __name__ == '__main__':
    unittest.main()
