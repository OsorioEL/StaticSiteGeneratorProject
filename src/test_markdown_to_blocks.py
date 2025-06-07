import unittest

from textnode import TextNode, TextType, text_node_to_html_node, split_nodes_delimter, extract_markdown_images, extract_markdown_links, markdown_to_blocks
from htmlnode import LeafNode, ParentNode, HTMLNode


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
        
    def test_empty_string(self):
        self.assertEqual(markdown_to_blocks(""), [])

    def test_whitespace_only(self):
        self.assertEqual(markdown_to_blocks("   \n  \n\n \n"), [])

    def test_single_paragraph(self):
        md = "Just a single paragraph without double newlines."
        self.assertEqual(markdown_to_blocks(md), ["Just a single paragraph without double newlines."])

    def test_multiple_paragraphs(self):
        md = "Paragraph one.\n\nParagraph two.\n\nParagraph three."
        self.assertEqual(
            markdown_to_blocks(md),
            ["Paragraph one.", "Paragraph two.", "Paragraph three."]
        )

    def test_paragraphs_with_extra_spaces(self):
        md = "  First paragraph with spaces.  \n\n  Second paragraph.  "
        self.assertEqual(
            markdown_to_blocks(md),
            ["First paragraph with spaces.", "Second paragraph."]
        )

    def test_mixed_newlines(self):
        md = "Line one\nLine two\n\nLine three\n\n\nLine four"
        self.assertEqual(
            markdown_to_blocks(md),
            ["Line one\nLine two", "Line three", "Line four"]
        )

    def test_trailing_and_leading_newlines(self):
        md = "\n\nStart\n\nMiddle\n\nEnd\n\n"
        self.assertEqual(
            markdown_to_blocks(md),
            ["Start", "Middle", "End"]
        )