import re
from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    # Initialize return list
    new_nodes = []
    # This function only operates on TextNodes with text_type == TEXT
    for node in old_nodes:
        if isinstance(node, TextNode):
            if node.text_type == TextType.TEXT:
                check = node.text.split(delimiter)
                if len(check) == 1:
                    # If no split, then no delimiters, just add node back
                    new_nodes.append(node)
                elif len(check) % 2 == 0:
                    raise Exception("split_nodes_delimiter: uneven number of delimeters found in node, invalid markdown")
                else:
                    while len(check) > 2:
                        # While there are more pairs of delimiters, keep splitting the nodes
                        before_text = check.pop(0)
                        new_nodes.append(TextNode(before_text, TextType.TEXT))
                        delimiter_text = check.pop(0)
                        new_nodes.append(TextNode(delimiter_text, text_type))
                    # Once finished, the last entry in check should go into a final text node
                    last_text = check.pop(0)
                    new_nodes.append(TextNode(last_text, TextType.TEXT))
                continue
        # Otherwise, just add the node to the new list without modifying it
        new_nodes.append(node)
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_image_positions(text):
    return re.finditer(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)

def extract_markdown_link_positions(text):
    return re.finditer(r"\[(.*?)\]\((.*?)\)", text)

def split_nodes_image(old_nodes):
    # Initialize return list
    new_nodes = []
    # This function only operates on TextNodes with text_type == TEXT
    for node in old_nodes:
        if isinstance(node, TextNode):
            if node.text_type == TextType.TEXT:
                check = extract_markdown_images(node.text)
                if len(check) == 0:
                    # If no links found, just add node back
                    new_nodes.append(node)
                else:
                    # Links were found, split
                    lastInd = 0
                    for match in extract_markdown_image_positions(node.text):
                        alt_text = match.group(1)
                        url = match.group(2)
                        start, end = match.span()
                        # Get text node before this match, since last match
                        new_nodes.append(TextNode(node.text[lastInd:start], TextType.TEXT))
                        # Get Link node as match
                        new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
                        lastInd = end
                    if lastInd < len(node.text):
                        # Append trailing text after last match
                        new_nodes.append(TextNode(node.text[lastInd:], TextType.TEXT))
                continue
        # Otherwise
        new_nodes.append(node)
    return new_nodes

def split_nodes_link(old_nodes):
    # Initialize return list
    new_nodes = []
    # This function only operates on TextNodes with text_type == TEXT
    for node in old_nodes:
        if isinstance(node, TextNode):
            if node.text_type == TextType.TEXT:
                check = extract_markdown_links(node.text)
                if len(check) == 0:
                    # If no links found, just add node back
                    new_nodes.append(node)
                else:
                    # Links were found, split
                    lastInd = 0
                    for match in extract_markdown_link_positions(node.text):
                        alt_text = match.group(1)
                        url = match.group(2)
                        start, end = match.span()
                        # Get text node before this match, since last match
                        new_nodes.append(TextNode(node.text[lastInd:start], TextType.TEXT))
                        # Get Link node as match
                        new_nodes.append(TextNode(alt_text, TextType.LINK, url))
                        lastInd = end
                    if lastInd < len(node.text):
                        # Append trailing text after last match
                        new_nodes.append(TextNode(node.text[lastInd:], TextType.TEXT))
                continue
        # Otherwise
        new_nodes.append(node)
    return new_nodes

def text_to_textnodes(text):
    new_nodes = [TextNode(text, TextType.TEXT)]
    new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_link(new_nodes)
    return new_nodes