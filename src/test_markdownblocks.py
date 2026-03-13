import unittest

from markdownblocks import (
    BlockType,
    markdown_to_blocks,
    block_to_block_type
)

class TestMarkdownBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_header_blocks(self):
        # No Header
        md0 = "This isn't a header"
        self.assertEqual(block_to_block_type(md0), BlockType.PARAGRAPH)
        # One Header
        md1 = "# This is a header"
        self.assertEqual(block_to_block_type(md1), BlockType.HEADING)
        # Two Header
        md2 = "## This is a header"
        self.assertEqual(block_to_block_type(md2), BlockType.HEADING)
        # Three Header
        md3 = "### This is a header"
        self.assertEqual(block_to_block_type(md3), BlockType.HEADING)
        # Four Header
        md4 = "##### This is a header"
        self.assertEqual(block_to_block_type(md4), BlockType.HEADING)
        # Five Header
        md5 = "##### This is a header"     
        self.assertEqual(block_to_block_type(md5), BlockType.HEADING)
        # Six Header
        md6 = "###### This is a header"
        self.assertEqual(block_to_block_type(md6), BlockType.HEADING)
        # Too many Header
        md7 = "####### This is not a header"
        self.assertEqual(block_to_block_type(md7), BlockType.PARAGRAPH)

    def test_code_blocks(self):
        # Not a code block
        md0 = """``
this is not a code block``"""
        self.assertEqual(block_to_block_type(md0), BlockType.PARAGRAPH)
        # Is a code block
        md1 = """```
this is a code block```"""
        self.assertEqual(block_to_block_type(md1), BlockType.CODE)
        # Is a code block
        md2 = """```
this is a code block
with multiple lines```"""
        self.assertEqual(block_to_block_type(md2), BlockType.CODE)
        # Not a code block
        md3 = """````
this is not a code block````"""
        self.assertEqual(block_to_block_type(md3), BlockType.CODE)

    def test_quote_blocks(self):
        # Not a quote block
        md0 = """not a quote"""
        self.assertEqual(block_to_block_type(md0), BlockType.PARAGRAPH)
        # Quote block
        md1 = """>> is a quote"""
        self.assertEqual(block_to_block_type(md1), BlockType.QUOTE)
        # Multi Quote block
        md2 = """>is a quote
> is also a quote
>third quote"""
        self.assertEqual(block_to_block_type(md2), BlockType.QUOTE)
        # Not a multi quote
        md3 = """> is a quote
is not a quote
>is a quote"""
        self.assertEqual(block_to_block_type(md3), BlockType.PARAGRAPH)

    def test_unordered_list_blocks(self):
        # not
        md0 = """not a list"""
        self.assertEqual(block_to_block_type(md0), BlockType.PARAGRAPH)
        # not
        md1 = """-not a list"""
        self.assertEqual(block_to_block_type(md1), BlockType.PARAGRAPH)
        # not
        md2 = """- is a list
-not a list
- is a list
-not a list"""
        self.assertEqual(block_to_block_type(md2), BlockType.PARAGRAPH)
        # is
        md3 = """- is a list"""
        self.assertEqual(block_to_block_type(md3), BlockType.UNORDERED_LIST)
        # is
        md4 = """- is a list
- is a list
- is a list"""
        self.assertEqual(block_to_block_type(md4), BlockType.UNORDERED_LIST)

    def test_ordered_list_blocks(self):
        # not
        md0 = """1 not a list"""
        self.assertEqual(block_to_block_type(md0), BlockType.PARAGRAPH)
        # not
        md1 = """1.not a list"""
        self.assertEqual(block_to_block_type(md1), BlockType.PARAGRAPH)
        # not
        md2 = """2. not a list"""
        self.assertEqual(block_to_block_type(md2), BlockType.PARAGRAPH)
        # not
        md3 = """1. is a list
2 not a list
3. is a list"""
        self.assertEqual(block_to_block_type(md3), BlockType.PARAGRAPH)
        md4 = """1. is a list
3. not a list"""
        self.assertEqual(block_to_block_type(md4), BlockType.PARAGRAPH)
        # is
        md5 = """1. is a list"""
        self.assertEqual(block_to_block_type(md5), BlockType.ORDERED_LIST)
        md6 = """1. is a list
2. is a list
3. is a list"""
        self.assertEqual(block_to_block_type(md6), BlockType.ORDERED_LIST)

if __name__ == "__main__":
    unittest.main()
