import unittest
from textnode import TextNode, TextType
from textnode import split_nodes_image, split_nodes_link

class TestSplitNodesFunctions(unittest.TestCase):

    def test_image_single(self):
        nodes = [TextNode("This is an image ![alt](https://img.com/image.png) end.", TextType.TEXT, None)]
        result = split_nodes_image(nodes)
        self.assertEqual(result, [
            TextNode("This is an image ", TextType.TEXT, None),
            TextNode("alt", TextType.IMAGE, "https://img.com/image.png"),
            TextNode(" end.", TextType.TEXT, None),
        ])

    def test_image_multiple(self):
        nodes = [TextNode("![first](url1) text ![second](url2)", TextType.TEXT, None)]
        result = split_nodes_image(nodes)
        self.assertEqual(result, [
            TextNode("", TextType.TEXT, None),
            TextNode("first", TextType.IMAGE, "url1"),
            TextNode(" text ", TextType.TEXT, None),
            TextNode("second", TextType.IMAGE, "url2"),
        ])

    def test_image_none(self):
        nodes = [TextNode("Just plain text without any images.", TextType.TEXT, None)]
        result = split_nodes_image(nodes)
        self.assertEqual(result, nodes)

    def test_link_single(self):
        nodes = [TextNode("This is a [link](https://example.com) in text.", TextType.TEXT, None)]
        result = split_nodes_link(nodes)
        self.assertEqual(result, [
            TextNode("This is a ", TextType.TEXT, None),
            TextNode("link", TextType.LINK, "https://example.com"),
            TextNode(" in text.", TextType.TEXT, None),
        ])

    def test_link_multiple(self):
        nodes = [TextNode("[Google](https://google.com) and [Bing](https://bing.com)", TextType.TEXT, None)]
        result = split_nodes_link(nodes)
        self.assertEqual(result, [
            TextNode("", TextType.TEXT, None),
            TextNode("Google", TextType.LINK, "https://google.com"),
            TextNode(" and ", TextType.TEXT, None),
            TextNode("Bing", TextType.LINK, "https://bing.com"),
        ])

    def test_link_none(self):
        nodes = [TextNode("No links here, just content.", TextType.TEXT, None)]
        result = split_nodes_link(nodes)
        self.assertEqual(result, nodes)

    def test_combined_links_and_images(self):
        # First, test images
        image_nodes = split_nodes_image([
            TextNode("Start ![img](url.png) mid ![img2](url2.png) end.", TextType.TEXT, None)
        ])
        self.assertEqual(image_nodes, [
            TextNode("Start ", TextType.TEXT, None),
            TextNode("img", TextType.IMAGE, "url.png"),
            TextNode(" mid ", TextType.TEXT, None),
            TextNode("img2", TextType.IMAGE, "url2.png"),
            TextNode(" end.", TextType.TEXT, None),
        ])

        # Then, test links
        link_nodes = split_nodes_link([
            TextNode("See [this](url) and [that](url2)", TextType.TEXT, None)
        ])
        self.assertEqual(link_nodes, [
            TextNode("See ", TextType.TEXT, None),
            TextNode("this", TextType.LINK, "url"),
            TextNode(" and ", TextType.TEXT, None),
            TextNode("that", TextType.LINK, "url2"),
        ])

    def test_edge_case_empty_string(self):
        nodes = [TextNode("", TextType.TEXT, None)]
        self.assertEqual(split_nodes_image(nodes), [TextNode("", TextType.TEXT, None)])
        self.assertEqual(split_nodes_link(nodes), [TextNode("", TextType.TEXT, None)])

    def test_edge_case_only_image(self):
        nodes = [TextNode("![alt](url)", TextType.TEXT, None)]
        self.assertEqual(split_nodes_image(nodes), [
            TextNode("", TextType.TEXT, None),
            TextNode("alt", TextType.IMAGE, "url")
        ])

    def test_edge_case_only_link(self):
        nodes = [TextNode("[text](url)", TextType.TEXT, None)]
        self.assertEqual(split_nodes_link(nodes), [
            TextNode("", TextType.TEXT, None),
            TextNode("text", TextType.LINK, "url")
        ])
