import unittest
from parsing_block import *
from block import *

class TestBlockParsing(unittest.TestCase):
    def test_markdown_to_blocks(self):
        input_markdown = """This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items"""

        self.assertEqual(markdown_to_blocks(input_markdown), [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ])
    def test_clock_to_block_type(self):
        cases = [
            ("header", "## Header", BlockType.HEADING),
            ("code", "```sdfsdfsdf\ndfbdfg\ndfgdfgdfg```", BlockType.CODE),
            ("quote", "> This is a quote\n>Frfr\n>No cap", BlockType.QUOTE),
            ("unordered list", "- This is a list\n- with items", BlockType.UNORDERED_LIST),
            ("ordered list", "1. This is a list\n2. with items", BlockType.ORDERED_LIST),
            ("paragraph", "```This is a paragraph", BlockType.PARAGRAPH)
        ]
        for label, block, expected in cases:
            with self.subTest(label=label):
                self.assertEqual(block_to_block_type(block), expected)



if __name__ == '__main__':
    unittest.main()
