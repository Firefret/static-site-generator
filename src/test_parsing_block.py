import unittest
from parsing_block import *

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


if __name__ == '__main__':
    unittest.main()
