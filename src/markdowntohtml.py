import os
from markdownblocks import (
    BlockType, 
    markdown_to_blocks, 
    block_to_block_type,)
from htmlnode import (
    LeafNode, 
    ParentNode,)
from splitdelims import (
    text_to_textnodes,
)
from textnode import (
    text_node_to_html_node,
)
from copydir import (
    read_file_to_string,
)

def markdown_to_html_node(markdown):
    out_nodes = []
    # Pseudocode:
    # Split markdown into markdown blocks
    # Loop through blocks
    #   Determine type of block
    #   Convert block to HTMLNode based on type
    #   Assign the proper child HTMLNode objects to the block node
    #     Create a shared text_to_children(text) function that works for all block types (TextNode -> HTMLNode)
    #     Code blocks are special and should not process inline markdown within themselves, don't use 
    #       text_to_children on this block, make a TextNode and just use text_node_to_html_node on it
    # Make all the block nodes children under a single parent HTML node which should be a div and return it
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.PARAGRAPH:
                # Want to replace newline characters with spaces
                pass_block = block.replace("\n", " ")
                html_nodes = text_nodes_to_html_nodes(text_to_textnodes(pass_block))
                out_nodes.append(ParentNode("p", html_nodes))
            case BlockType.HEADING:
                # Heading block tag is h1 - h6 depending on number of # characters
                heading_tag = heading_line_to_heading_tag(block)
                html_nodes = text_nodes_to_html_nodes(text_to_textnodes(heading_line_to_string(block)))
                out_nodes.append(ParentNode(heading_tag, html_nodes))
            case BlockType.CODE:
                # Code block ignores markdown text node parsing, needs to be wrapped in nested html
                # <pre><code> code block here </code></pre>
                code_text = block[4:-3] # Remove ```\n at start and ``` at end
                child = LeafNode("code", code_text)
                out_nodes.append(ParentNode("pre", [child]))
            case BlockType.QUOTE:
                html_nodes = text_nodes_to_html_nodes(text_to_textnodes(remove_leading_from_blockquote(block)))
                out_nodes.append(ParentNode("blockquote", html_nodes))
            case BlockType.UNORDERED_LIST:
                out_nodes.append(ParentNode("ul", unordered_list_block_to_html_list_nodes(block)))
            case BlockType.ORDERED_LIST:
                out_nodes.append(ParentNode("ol", ordered_list_block_to_html_list_nodes(block)))
    # Wrap everything in a parentnode div
    return ParentNode("div", out_nodes)

def text_nodes_to_html_nodes(in_nodes):
    out_nodes = []
    for node in in_nodes:
        out_nodes.append(text_node_to_html_node(node))
    return out_nodes

def heading_line_to_heading_tag(text):
    count = len(text) - len(text.lstrip("#"))

    if 1 <= count <= 6:
        return f"h{count}"
    
    raise ValueError("Not a valid markdown heading")

def heading_line_to_string(text):
    return text.lstrip("#").strip()

def remove_leading_from_blockquote(text):
    out_lines = []
    for line in text.splitlines():
        out_lines.append(line[2:])
    return "\n".join(out_lines)

def unordered_list_block_to_html_list_nodes(text):
    list_nodes = []
    for line in text.splitlines():
        html_nodes = text_nodes_to_html_nodes(text_to_textnodes(line[2:]))
        list_nodes.append(ParentNode("li", html_nodes))
    return list_nodes

def ordered_list_block_to_html_list_nodes(text):
    list_nodes = []
    for line in text.splitlines():
        html_nodes = text_nodes_to_html_nodes(text_to_textnodes(line[3:]))
        list_nodes.append(ParentNode("li", html_nodes))
    return list_nodes

def extract_markdown_header(text):
    lines = text.splitlines()
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("No h1 header found in markdown text")

def replace_text_with_block(original_text, find_text, replace_text):
    return original_text.replace(find_text, replace_text)

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown = read_file_to_string(from_path)
    #print(f"Markdown read from file: \n\n{markdown}")
    template = read_file_to_string(template_path)
    #print(f"Template read from file:\n\n{template}")
    html_node = markdown_to_html_node(markdown)
    html_string = html_node.to_html()
    #print(f"HTML String after converting Markdown to HTML:\n\n{html_string}")
    header_string = extract_markdown_header(markdown)
    template = replace_text_with_block(template, "{{ Title }}", header_string)
    template = replace_text_with_block(template, "{{ Content }}", html_string)
    template = replace_text_with_block(template, 'href="/', f'href="{basepath}')
    template = replace_text_with_block(template, 'src="/', f'src="{basepath}')
    #print(f"Final template replaced string:\n\n{template}")
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for entry in os.listdir(dir_path_content):
        src_path = os.path.join(dir_path_content, entry)
        dest_path = os.path.join(dest_dir_path, entry)

        if os.path.isdir(src_path):
            # recreate directory in destination
            os.makedirs(dest_path, exist_ok=True)

            # recurse into directory
            generate_pages_recursive(src_path, template_path, dest_path, basepath)

        elif entry.endswith(".md"):
            # change extension to html
            dest_file = os.path.splitext(dest_path)[0] + ".html"

            # Generate page
            generate_page(src_path, template_path, dest_file, basepath)
