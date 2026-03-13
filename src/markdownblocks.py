from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    # Function to separate a full markdown document (passed in as a string)
    # into separate blocks based on double newline characters
    blocks = []
    raw_blocks = markdown.split('\n\n')
    for block in raw_blocks:
        cleaned = block.strip()
        if cleaned:
            blocks.append(cleaned)
    return blocks

def block_to_block_type(block):
    if re.match(r"^#{1,6} ", block):
        # Looking for 1-6 '#' characters = heading, html tag is <h1> - <h6>
        return BlockType.HEADING
    if re.match(r"^```[\s\S]*?```$", block):
        # Looking for starts with ``` and ends with ``` = code, html tag is <pre><code>
        return BlockType.CODE
    if re.match(r"^(?:> ?.*(?:\n|$))+$", block):
        # Looking for starts wtih '> ' = quote, html tag is <blockquote>
        return BlockType.QUOTE
    if re.match(r"^(?:- .+(?:\n|$))+$", block):
        # Looking for every line starts with '- ' = unordered list, html tag is <ul><li>
        return BlockType.UNORDERED_LIST
    if is_ordered_list_block(block):
        # Looking for every line starts with '1. ' in order = ordered list, html tag is <ol><li>
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def is_ordered_list_block(block: str) -> bool:
    lines = block.splitlines()
    expected_number = 1
    for line in lines:
        match = re.match(r'^(\d+)\. (.+)', line)
        if not match:
            return False
        number = int(match.group(1))
        if number != expected_number:
            return False
        expected_number += 1
    return True