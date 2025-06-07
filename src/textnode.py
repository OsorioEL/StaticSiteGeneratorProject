from enum import Enum
from htmlnode import HTMLNode, LeafNode, ParentNode
import re
class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self,text,text_type,url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, node2):
        if ((self.text == node2.text) and 
                (self.text_type == node2.text_type) and
            (self.url == node2.url)):
            return True
        else:
            return False

    def __repr__(self):
        return(f"TextNode({self.text},{self.text_type.value},{self.url})")
    
def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode("strong", text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    elif text_node.text_type == TextType.LINK and text_node.url:
        return LeafNode("a", text_node.text, props={"href": text_node.url})
    elif text_node.text_type == TextType.IMAGE and text_node.url:
        return LeafNode("img", "", props={"src": text_node.url, "alt": text_node.text})
    else:
        raise ValueError(f"Unsupported TextType: {text_node.text_type}")
    
def split_nodes_delimter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        parts = node.text.split(delimiter)
        if len(parts) % 2 == 0:
            raise Exception(f"Unmatched delimiter in: {node.text}")

        for i, part in enumerate(parts):
            if i % 2 == 0:
                new_nodes.append(TextNode(part, TextType.TEXT, node.url))
            else:
                new_nodes.append(TextNode(part, text_type, node.url))
    return new_nodes




def extract_markdown_images(text):
    import re
    image_pattern = re.compile(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)")
    matches = image_pattern.findall(text)
    images = []
    for alt_text, url in matches:
        images.append((alt_text, url))
    return images

def extract_markdown_links(text):
    import re
    link_pattern = re.compile(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)")
    matches = link_pattern.findall(text)
    links = []
    for text, url in matches:
        links.append((text, url))
    return links


import re

def split_nodes_image(old_nodes):
    new_nodes = []
    image_pattern = r'!\[(.*?)\]\((.*?)\)'

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        matches = list(re.finditer(image_pattern, node.text))
        last_index = 0

        if not matches:
            new_nodes.append(node)
            continue

        if matches[0].start() == 0:
            new_nodes.append(TextNode("", TextType.TEXT, None))

        for match in matches:
            start, end = match.span()
            alt_text, url = match.groups()

            before = node.text[last_index:start]
            if before:
                new_nodes.append(TextNode(before, TextType.TEXT, None))
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
            last_index = end

        after = node.text[last_index:]
        if after:
            new_nodes.append(TextNode(after, TextType.TEXT, None))

    return new_nodes

import re

def split_nodes_link(old_nodes):
    new_nodes = []
    link_pattern = r'(?<!!)\[(.*?)\]\((.*?)\)'

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        matches = list(re.finditer(link_pattern, node.text))
        last_index = 0

        # 🔧 This handles the case of a node with no content or no matches
        if not matches:
            new_nodes.append(node)
            continue

        if matches[0].start() == 0:
            new_nodes.append(TextNode("", TextType.TEXT, None))

        for match in matches:
            start, end = match.span()
            link_text, url = match.groups()

            before = node.text[last_index:start]
            if before:
                new_nodes.append(TextNode(before, TextType.TEXT, None))

            new_nodes.append(TextNode(link_text, TextType.LINK, url))
            last_index = end

        after = node.text[last_index:]
        if after:
            new_nodes.append(TextNode(after, TextType.TEXT, None))

    return new_nodes



# Text to nodes function which processes a string of test and returns a list of TextNodes with their correspoding (text, text_type, url) values. Using functions like split_nodes_image and split_nodes_link to process the text.
def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT, None)]
    nodes = split_nodes_image(nodes)                     # first
    nodes = split_nodes_link(nodes)                      # second
    nodes = split_nodes_delimter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimter(nodes, "`", TextType.CODE)
    return nodes

def markdown_to_blocks(text):
    """
    Splits text into blocks separated by double newlines.
    """
    blocks = text.split("\n\n")
    return [block.strip() for block in blocks if block.strip()]

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"
    
def block_to_block_type(block):
    """
    Determines the type of a block based on its content.
    """
    if block.startswith("# "):
        return BlockType.HEADING
    elif block.startswith("```"):
        return BlockType.CODE
    elif block.startswith(">"):  # Changed from '> ' to '>'
        return BlockType.QUOTE
    elif block.startswith("- ") or block.startswith("* "):
        return BlockType.UNORDERED_LIST
    elif re.match(r"^\d+\. ", block):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH
