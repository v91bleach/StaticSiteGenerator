import sys
from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from copydir import copy_dir, delete_contents
from markdowntohtml import generate_pages_recursive

def main():
    if len(sys.argv) >= 2:
        basepath = sys.argv[1]
    public_dir = "docs"
    static_dir = "static"
    # Delete existing /public data
    delete_contents(public_dir)
    # Copy /static data into /public folder
    copy_dir(static_dir, public_dir)
    # Write new full HTML page
    generate_pages_recursive("content", "template.html", "docs", basepath)

main()