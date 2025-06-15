import unittest
from markdown_blocks import markdown_to_html_node

class TestMarkdownConversion(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <strong>bolded</strong> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = "```\nLine with _italic_ syntax\nLine with **bold** syntax\nLine with [links](https://example.com)\n```"
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><pre><code>Line with _italic_ syntax\n"
            "Line with **bold** syntax\n"
            "Line with [links](https://example.com)</code></pre></div>"
        )
