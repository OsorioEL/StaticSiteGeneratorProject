import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
        
    def test_parent_node_with_no_children(self):
        with self.assertRaises(ValueError):
            ParentNode("div", []).to_html()

    def test_parent_node_with_multiple_children(self):
        child1 = LeafNode("p", "Hello")
        child2 = LeafNode("p", "World")
        parent_node = ParentNode("div", [child1, child2])
        self.assertEqual(parent_node.to_html(), "<div><p>Hello</p><p>World</p></div>")
        
    def test_parent_node_with_props(self):
        child = LeafNode("p", "Hello")
        parent_node = ParentNode("section", [child], props={"id": "main"})
        self.assertEqual(parent_node.to_html(), '<section id="main"><p>Hello</p></section>')

    def test_deeply_nested_nodes(self):
        node = ParentNode("div", [
            ParentNode("ul", [
                ParentNode("li", [LeafNode(None, "Item 1")]),
                ParentNode("li", [LeafNode(None, "Item 2")]),
            ])
        ])
        self.assertEqual(node.to_html(), "<div><ul><li>Item 1</li><li>Item 2</li></ul></div>")

    def test_leaf_node_without_tag(self):
        node = LeafNode(None, "Just text")
        self.assertEqual(node.to_html(), "Just text")
        
    def test_leaf_node_with_multiple_props(self):
        node = LeafNode("img", "", props={"src": "image.png", "alt": "An image"})
        self.assertEqual(node.to_html(), '<img src="image.png" alt="An image"></img>')
        
    def test_leaf_node_invalid(self):
        with self.assertRaises(ValueError):
            LeafNode(None, None)
            
    
    def test_mixed_leaf_nodes(self):
        node = ParentNode("p", [
            LeafNode(None, "Hello "),
            LeafNode("b", "world"),
            LeafNode(None, "!")
        ])
        self.assertEqual(node.to_html(), "<p>Hello <b>world</b>!</p>")



