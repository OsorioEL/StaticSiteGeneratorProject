import unittest

from textnode import TextNode, TextType, text_node_to_html_node, split_nodes_delimter, extract_markdown_images, extract_markdown_links, block_to_block_type, markdown_to_blocks
from textnode import BlockType
from htmlnode import LeafNode, ParentNode, HTMLNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
        
    def test_text_equal(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
        
    def test_text_not_equal(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a different text node", TextType.BOLD)
        self.assertNotEqual(node, node2)
        
    def test_text_type_equal(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node.text_type, node2.text_type)
        
    def test_text_type_not_equal(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node.text_type, node2.text_type)
        
    def test_url_none_vs_not_none(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
        self.assertNotEqual(node.url, node2.url)    
        
    def test_url_equal(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
        node2 = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
        self.assertEqual(node.url, node2.url)
        
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        
    def test_split_nodes_delimiter_single_node(self):
        node = TextNode("This is a text node with delimiters", TextType.TEXT)
        delimiter = " "
        text_type = TextType.TEXT
        new_nodes = split_nodes_delimter([node], delimiter, text_type)
        self.assertEqual(len(new_nodes), 7)
        self.assertEqual(new_nodes[0].text, "This")
        self.assertEqual(new_nodes[1].text, "is")
        self.assertEqual(new_nodes[2].text, "a")
        self.assertEqual(new_nodes[3].text, "text")
        self.assertEqual(new_nodes[4].text, "node")
        self.assertEqual(new_nodes[5].text, "with")
        self.assertEqual(new_nodes[6].text, "delimiters")
        
    def test_split_nodes_delimiter_with_list_of_nodes(self):
            node1 = TextNode("This is a text inline `code` text", TextType.TEXT)
            node2 = TextNode("Another text node with inline `again, code` 'text", TextType.TEXT)
            delimiter = "`"
            text_type = TextType.CODE  # ✅ Correct now
            new_nodes = split_nodes_delimter([node1, node2], delimiter, text_type)

            self.assertEqual(new_nodes[0], TextNode("This is a text inline ", TextType.TEXT))
            self.assertEqual(new_nodes[1], TextNode("code", TextType.CODE))
            self.assertEqual(new_nodes[2], TextNode(" text", TextType.TEXT))
            self.assertEqual(new_nodes[3], TextNode("Another text node with inline ", TextType.TEXT))
            self.assertEqual(new_nodes[4], TextNode("again, code", TextType.CODE))
            self.assertEqual(new_nodes[5], TextNode(" 'text", TextType.TEXT))

        
    def test_split_nodes_delimiter_raises_exception_on_even_split(self):
        node = TextNode("This is a text node uneven `code delimiters", TextType.TEXT)
        delimiter = "`"
        text_type = TextType.TEXT
        with self.assertRaises(Exception) as context:
            split_nodes_delimter([node], delimiter, text_type)
        self.assertTrue("Unmatched delimiter in: This is a text node uneven `code delimiters" in str(context.exception))
        
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    def test_block_to_block_type_heading(self):
        self.assertEqual(block_to_block_type("# Heading 1"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("# Another heading"), BlockType.HEADING)

    def test_block_to_block_type_code(self):
        self.assertEqual(block_to_block_type("```python\nprint('hi')\n```"), BlockType.CODE)
        self.assertEqual(block_to_block_type("```"), BlockType.CODE)

    def test_block_to_block_type_quote(self):
        self.assertEqual(block_to_block_type("> This is a quote"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type(">Another quote"), BlockType.QUOTE)

    def test_block_to_block_type_unordered_list(self):
        self.assertEqual(block_to_block_type("- item 1"), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type("* item 2"), BlockType.UNORDERED_LIST)

    def test_block_to_block_type_ordered_list(self):
        self.assertEqual(block_to_block_type("1. First item"), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type("23. Another item"), BlockType.ORDERED_LIST)

    def test_block_to_block_type_paragraph(self):
        self.assertEqual(block_to_block_type("Just a normal paragraph."), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("Another line of text."), BlockType.PARAGRAPH)

        
        
