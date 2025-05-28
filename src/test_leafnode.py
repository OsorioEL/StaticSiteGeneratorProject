import unittest

from htmlnode import HTMLNode, LeafNode


class TestLeafNode(unittest.TestCase):
        
    def test_node_no_arguments(self):
        with self.assertRaises(ValueError) as context:
            LeafNode(None, None)
        self.assertEqual(str(context.exception), "All leaf nodes must have a value")
        
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
        
    def test_leaf_to_html_with_props(self):
        node = LeafNode("span", "Hello, world!", props={"class": "highlight"})
        self.assertEqual(node.to_html(), '<span class="highlight">Hello, world!</span>')
        
  

if __name__ == "__main__":
    unittest.main()
