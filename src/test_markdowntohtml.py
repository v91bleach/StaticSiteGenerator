import unittest

from markdowntohtml import markdown_to_html_node, extract_markdown_header

class TestMarkdownToHtml(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_extract_markdown_header(self):
        md = """
This is a line of text
# This is header
Other text
"""
        check = extract_markdown_header(md)
        self.assertEqual(check, "This is header")
        md = """There is no header"""
        with self.assertRaises(Exception) as cm: extract_markdown_header(md)
        self.assertEqual(str(cm.exception), "No h1 header found in markdown text")

if __name__ == "__main__":
    unittest.main()