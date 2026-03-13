import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHtmlNode(unittest.TestCase):
    def test_init_tag(self):
        node = HTMLNode("p")
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, None)
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)
    
    def test_init_value(self):
        node = HTMLNode(None, "text")
        self.assertEqual(node.tag, None)
        self.assertEqual(node.value, "text")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)

    def test_init_children(self):
        child0 = HTMLNode("p")
        child1 = HTMLNode("a")
        child2 = HTMLNode("h1")
        node = HTMLNode(None, None, [child0, child1, child2])
        self.assertEqual(node.tag, None)
        self.assertEqual(node.value, None)
        self.assertEqual(node.children[0], child0)
        self.assertEqual(node.children[1], child1)
        self.assertEqual(node.children[2], child2)
        self.assertEqual(node.props, None)

    def test_init_props(self):
        props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        node = HTMLNode(None, None, None, props)
        self.assertEqual(node.tag, None)
        self.assertEqual(node.value, None)
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, props)

    def test_init_all(self):
        child0 = HTMLNode("p")
        child1 = HTMLNode("a")
        child2 = HTMLNode("h1")
        props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        node = HTMLNode("p", "text", [child0, child1, child2], props)
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "text")
        self.assertEqual(node.children[0], child0)
        self.assertEqual(node.children[1], child1)
        self.assertEqual(node.children[2], child2)
        self.assertEqual(node.props, props)

    def test_props_to_html(self):
        props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        node = HTMLNode(None, None, None, props)
        check = node.props_to_html()
        expected = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(check, expected)

    def test_init(self):
        props = {
                    "href": "https://www.google.com",
                    "target": "_blank",
                }
        node = LeafNode("p", "text", props)
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "text")
        self.assertEqual(node.props, props)

    def test_no_tag(self):
        node = LeafNode(None, "text")
        self.assertEqual(node.to_html(), "text")

    def test_p_tag(self):
        node = LeafNode("p", "text")
        self.assertEqual(node.to_html(), "<p>text</p>")

    def test_a_tag(self):
        node = LeafNode("a", "text")
        self.assertEqual(node.to_html(), "<a>text</a>")

    def test_h1_tag(self):
        node = LeafNode("h1", "text")
        self.assertEqual(node.to_html(), "<h1>text</h1>")

    def test_href_props(self):
        props = {
                    "href": "https://www.google.com",
                    "target": "_blank",
                }
        node = LeafNode("a", "text", props)
        self.assertEqual(node.to_html(), '<a href="https://www.google.com" target="_blank">text</a>')

    def test_to_html_no_children(self):
        parent = ParentNode("div", None)
        with self.assertRaises(ValueError) as cm: parent.to_html()
        self.assertEqual(str(cm.exception), "No children")

    def test_to_html_no_tag(self):
        child = LeafNode("span", "child")
        parent = ParentNode(None, [child])
        with self.assertRaises(ValueError) as cm: parent.to_html()
        self.assertEqual(str(cm.exception), "No tag")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_children_props(self):
        props = {
                    "href": "https://www.google.com",
                    "target": "_blank",
                }
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node], props)
        self.assertEqual(parent_node.to_html(), '<div href="https://www.google.com" target="_blank"><span>child</span></div>')
        child_node = LeafNode("span", "child", props)
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), '<div><span href="https://www.google.com" target="_blank">child</span></div>')

    def test_to_html_with_grandchildren_props(self):
        props = {
                    "href": "https://www.google.com",
                    "target": "_blank",
                }
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node], props)
        self.assertEqual(parent_node.to_html(), '<div href="https://www.google.com" target="_blank"><span><b>grandchild</b></span></div>')
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node], props)
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), '<div><span href="https://www.google.com" target="_blank"><b>grandchild</b></span></div>')
        grandchild_node = LeafNode("b", "grandchild", props)
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), '<div><span><b href="https://www.google.com" target="_blank">grandchild</b></span></div>')

    def test_to_html_many_children(self):
        child0 = LeafNode("b", "child")
        child1 = LeafNode("p", "child")
        child2 = LeafNode("span", "child")
        child3 = LeafNode(None, "text")
        parent = ParentNode("div", [child0, child1, child2, child3])
        self.assertEqual(parent.to_html(), "<div><b>child</b><p>child</p><span>child</span>text</div>")

if __name__ == "__main__":
    unittest.main()