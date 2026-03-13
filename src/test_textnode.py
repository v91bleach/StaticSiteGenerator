import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.TEXT)
        self.assertEqual(node, node2)

    def test_eq_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        node2 = TextNode("This is a bold node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_italic(self):
        node = TextNode("This is a italic node", TextType.ITALIC)
        node2 = TextNode("This is a italic node", TextType.ITALIC)
        self.assertEqual(node, node2)

    def test_eq_code(self):
        node = TextNode("This is a code node", TextType.CODE)
        node2 = TextNode("This is a code node", TextType.CODE)
        self.assertEqual(node, node2)

    def test_eq_link(self):
        node = TextNode("This is a link node", TextType.LINK, "https://www.link.html")
        node2 = TextNode("This is a link node", TextType.LINK, "https://www.link.html")
        self.assertEqual(node, node2)
        
    def test_eq_image(self):
        node = TextNode("This is a image node", TextType.IMAGE, "https://www.link.jpg")
        node2 = TextNode("This is a image node", TextType.IMAGE, "https://www.link.jpg")
        self.assertEqual(node, node2)

    def test_neq_text_bold(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a bold node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_neq_bold_italic(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        node2 = TextNode("This is a italic node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_neq_italic_code(self):
        node = TextNode("This is a italic node", TextType.ITALIC)
        node2 = TextNode("This is a code node", TextType.CODE)
        self.assertNotEqual(node, node2)

    def test_neq_code_link(self):
        node = TextNode("This is a code node", TextType.CODE)
        node2 = TextNode("This is a link node", TextType.LINK, "https://www.link.html")
        self.assertNotEqual(node, node2)

    def test_neq_link_image(self):
        node = TextNode("This is a link node", TextType.LINK, "https://www.link.html")
        node2 = TextNode("This is a image node", TextType.IMAGE, "https://www.link.jpg")
        self.assertNotEqual(node, node2)

    def test_text_to_html_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_text_to_html_bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a text node")

    def test_text_to_html_italic(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a text node")

    def test_text_to_html_code(self):
        node = TextNode("This is a text node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a text node")

    def test_text_to_html_link(self):
        node = TextNode("This is a text node", TextType.LINK, "https://www.link.html")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.props, {"href": "https://www.link.html"})

    def test_text_to_html_link(self):
        node = TextNode("This is a text node", TextType.IMAGE, "https://www.link.html")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "https://www.link.html", "alt": "This is a text node"})

if __name__ == "__main__":
    unittest.main()
