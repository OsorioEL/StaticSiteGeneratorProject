import unittest
from textnode import extract_markdown_images, extract_markdown_links

class TestMarkdownFunctions(unittest.TestCase):

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_multiple_markdown_images(self):
        matches = extract_markdown_images(
            "Image one ![img1](url1.png) and two ![img2](url2.jpg)"
        )
        self.assertListEqual([("img1", "url1.png"), ("img2", "url2.jpg")], matches)

    def test_extract_image_with_empty_alt_text(self):
        matches = extract_markdown_images("Empty alt ![](https://img.com/blank.png)")
        self.assertListEqual([("", "https://img.com/blank.png")], matches)

    def test_extract_image_with_special_characters(self):
        matches = extract_markdown_images(
            "Image: ![complex (alt)!@#](http://example.com/img.png)"
        )
        self.assertListEqual([("complex (alt)!@#", "http://example.com/img.png")], matches)

    def test_extract_no_markdown_images(self):
        matches = extract_markdown_images("This has no images.")
        self.assertListEqual([], matches)

    def test_extract_malformed_image_syntax(self):
        matches = extract_markdown_images("Broken ![image(https://bad.com/img.png)")
        self.assertListEqual([], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://example.com)"
        )
        self.assertListEqual([("link", "https://example.com")], matches)

    def test_extract_multiple_markdown_links(self):
        matches = extract_markdown_links(
            "[Google](https://google.com) and [GitHub](https://github.com)"
        )
        self.assertListEqual([
            ("Google", "https://google.com"),
            ("GitHub", "https://github.com")
        ], matches)

    def test_extract_link_with_empty_text(self):
        matches = extract_markdown_links("Empty link: [](https://example.com)")
        self.assertListEqual([("", "https://example.com")], matches)

    def test_extract_link_ignores_image(self):
        matches = extract_markdown_links(
            "This is an image: ![notalink](https://example.com/img.png)"
        )
        self.assertListEqual([], matches)

    def test_extract_link_with_special_characters(self):
        matches = extract_markdown_links(
            "Special [params & symbols](https://example.com/?a=1&b=2)"
        )
        self.assertListEqual(
            [("params & symbols", "https://example.com/?a=1&b=2")],
            matches
        )

    def test_extract_malformed_link_syntax(self):
        matches = extract_markdown_links("Broken [link](https://example.com")
        self.assertListEqual([], matches)