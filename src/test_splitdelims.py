import unittest

from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from splitdelims import (
    split_nodes_delimiter, 
    extract_markdown_images, 
    extract_markdown_links, 
    extract_markdown_image_positions, 
    extract_markdown_link_positions, 
    split_nodes_image, split_nodes_link, 
    text_to_textnodes, 
)


class TestSplitDelims(unittest.TestCase):
    def test_no_text_nodes(self):
        gchild = LeafNode("p", "text")
        child = ParentNode("b", [gchild])
        parent = ParentNode("i", [child])
        leaf0 = LeafNode("b", "text")
        leaf1 = LeafNode("i", "text")
        node_list = [parent, leaf0, leaf1]
        new_nodes = split_nodes_delimiter(node_list, "**", TextType.BOLD)
        self.assertEqual(new_nodes[0], parent)
        self.assertEqual(new_nodes[1], leaf0)
        self.assertEqual(new_nodes[2], leaf1)

    def test_split_bold1(self):
        node = TextNode("This is a **bold** test", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0], TextNode("This is a ", TextType.TEXT))
        self.assertEqual(new_nodes[1], TextNode("bold", TextType.BOLD))
        self.assertEqual(new_nodes[2], TextNode(" test", TextType.TEXT))

    def test_split_bold_uneven(self):
        node = TextNode("This is a **bad test", TextType.TEXT)
        with self.assertRaises(Exception) as cm: split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(str(cm.exception), "split_nodes_delimiter: uneven number of delimeters found in node, invalid markdown")

    def test_split_bold_uneven_multi(self):
        node = TextNode("This is a **bold** **bad test", TextType.TEXT)
        with self.assertRaises(Exception) as cm: split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(str(cm.exception), "split_nodes_delimiter: uneven number of delimeters found in node, invalid markdown")

    def test_split_bold2(self):
        node = TextNode("This is a **bold** test, **very bold** indeed", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 5)
        self.assertEqual(new_nodes[0], TextNode("This is a ", TextType.TEXT))
        self.assertEqual(new_nodes[1], TextNode("bold", TextType.BOLD))
        self.assertEqual(new_nodes[2], TextNode(" test, ", TextType.TEXT))
        self.assertEqual(new_nodes[3], TextNode("very bold", TextType.BOLD))
        self.assertEqual(new_nodes[4], TextNode(" indeed", TextType.TEXT))

    def test_split_italic1(self):
        node = TextNode("This is a _italic_ test", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0], TextNode("This is a ", TextType.TEXT))
        self.assertEqual(new_nodes[1], TextNode("italic", TextType.ITALIC))
        self.assertEqual(new_nodes[2], TextNode(" test", TextType.TEXT))
                                                
    def test_split_code1(self):
        node = TextNode("This is a `code` test", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0], TextNode("This is a ", TextType.TEXT))
        self.assertEqual(new_nodes[1], TextNode("code", TextType.CODE))
        self.assertEqual(new_nodes[2], TextNode(" test", TextType.TEXT))

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_multi_images(self):
        matches = extract_markdown_images(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        self.assertListEqual([("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")], matches)

    def test_extract_markdown_no_images(self):
        matches = extract_markdown_images("This is text with no images")
        self.assertListEqual([], matches)

    def test_extract_markdown_link(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev")], matches)

    def test_extract_markdown_multi_link(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)

    def test_extract_markdown_no_links(self):
        matches = extract_markdown_links("This is text with no links")
        self.assertListEqual([], matches)

    def test_extract_markdown_image_positions_no_images(self):
        matches = list(extract_markdown_image_positions("This is text with no images"))
        self.assertListEqual([], matches)

    def test_extract_markdown_image_positions_single(self):
        matches = list(extract_markdown_image_positions(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        ))
        firstMatch = matches[0]
        self.assertEqual(firstMatch.group(1), 'image')
        self.assertEqual(firstMatch.group(2), 'https://i.imgur.com/zjjcJKZ.png')
        self.assertEqual(firstMatch.start(), len("This is text with an "))
        self.assertEqual(firstMatch.end(), len(firstMatch.string))

    def test_extract_markdown_image_positions_multi(self):
        matches = list(extract_markdown_image_positions(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        ))
        firstMatch = matches[0]
        self.assertEqual(firstMatch.group(1), 'rick roll')
        self.assertEqual(firstMatch.group(2), 'https://i.imgur.com/aKaOqIh.gif')
        self.assertEqual(firstMatch.start(), len("This is text with a "))
        self.assertEqual(firstMatch.end(), len("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif)"))

        secondMatch = matches[1]
        self.assertEqual(secondMatch.group(1), 'obi wan')
        self.assertEqual(secondMatch.group(2), 'https://i.imgur.com/fJRm4Vk.jpeg')
        self.assertEqual(secondMatch.start(), len("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and "))
        self.assertEqual(secondMatch.end(), len(secondMatch.string))

    def test_extract_markdown_link_positions_no_links(self):
        matches = list(extract_markdown_link_positions("THis is text with no links"))
        self.assertListEqual([], matches)

    def test_extract_markdown_link_positions_single(self):
        matches = list(extract_markdown_link_positions(
            "This is text with a link [to boot dev](https://www.boot.dev)"
        ))
        firstMatch = matches[0]
        self.assertEqual(firstMatch.group(1), 'to boot dev')
        self.assertEqual(firstMatch.group(2), 'https://www.boot.dev')
        self.assertEqual(firstMatch.start(), len("This is text with a link "))
        self.assertEqual(firstMatch.end(), len(firstMatch.string))

    def test_extract_markdown_link_positions_multi(self):
        matches = list(extract_markdown_link_positions(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        ))
        firstMatch = matches[0]
        self.assertEqual(firstMatch.group(1), 'to boot dev')
        self.assertEqual(firstMatch.group(2), 'https://www.boot.dev')
        self.assertEqual(firstMatch.start(), len("This is text with a link "))
        self.assertEqual(firstMatch.end(), len("This is text with a link [to boot dev](https://www.boot.dev)"))

        secondMatch = matches[1]
        self.assertEqual(secondMatch.group(1), 'to youtube')
        self.assertEqual(secondMatch.group(2), 'https://www.youtube.com/@bootdotdev')
        self.assertEqual(secondMatch.start(), len("This is text with a link [to boot dev](https://www.boot.dev) and "))
        self.assertEqual(secondMatch.end(), len(secondMatch.string))

    def test_split_images_no_image(self):
        node = TextNode(
            "This is text with no images",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with no images", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_images_single(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_images_no_trail(self):
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

    def test_split_images_with_trail(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) and trailing text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
                TextNode(" and trailing text", TextType.TEXT)
            ],
            new_nodes,
        )

    def test_split_links_no_link(self):
        node = TextNode(
            "This is text with no links",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with no links", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links_sinlge(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            ],
            new_nodes,
        )


    def test_split_links_no_trail(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            ],
            new_nodes,
        )


    def test_split_links_with_trail(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev) and trailing text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
                TextNode(" and trailing text", TextType.TEXT)
            ],
            new_nodes,
        )

    def test_split_text_to_textnodes(self):
        nodes = text_to_textnodes("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            nodes
        )

if __name__ == "__main__":
    unittest.main()
