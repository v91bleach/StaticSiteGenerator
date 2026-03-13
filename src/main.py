from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from copydir import copy_dir, delete_contents
from markdowntohtml import generate_pages_recursive

def main():
    public_dir = "public"
    static_dir = "static"
    # Delete existing /public data
    delete_contents(public_dir)
    # Copy /static data into /public folder
    copy_dir(static_dir, public_dir)
    # Write new full HTML page
    generate_pages_recursive("content", "template.html", "public")

main()