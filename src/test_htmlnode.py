import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
        
    def test_node_no_arguments(self):
        node =HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)
        
    def test_props_to_html_with_props(self):
        node =HTMLNode(tag='div',props={"class": "container", "id": "main"})
        expected_props = 'class="container" id="main"'
        self.assertEqual(node.props_to_html(), expected_props)
        
    def test_props_to_html_when_No_Props(self):
        node =HTMLNode()
        self.assertEqual(node.props_to_html(),"")
        

if __name__ == "__main__":
    unittest.main()
