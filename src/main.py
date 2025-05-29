from textnode import TextNode
from textnode import TextType
from htmlnode import LeafNode, ParentNode
from htmlnode import HTMLNode

def main():
    new_text_node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(repr(new_text_node))
    new_html_node = HTMLNode("div", "Hello, world!", props={"class": "container"})
    print(repr(new_html_node))
    new_leaf_node = LeafNode("p", "This is a paragraph.", props={"class": "text"})
    print(repr(new_leaf_node))
    new_parent_node = ParentNode("div", [new_leaf_node, new_text_node], props={"id": "main"})
    print(repr(new_parent_node))



if __name__ == "__main__":
    main()
