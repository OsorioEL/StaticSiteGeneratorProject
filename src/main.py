from textnode import TextNode
from textnode import TextType
from htmlnode import LeafNode, ParentNode
from htmlnode import HTMLNode

def main():
    new_text_node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(repr(new_text_node))
    new_html_node = HTMLNode("div", "Hello, world!", props={"class": "container"})
    print(repr(new_html_node))
    print()
    new_leaf_node = LeafNode("p", "This is a paragraph.", props={"class": "text"})
    print(repr(new_leaf_node))
    print(new_leaf_node.to_html())
    print()
    new_input_node = LeafNode(
        "input",
        "",  # Or None if your class handles that for self-closing tags
        props={
            "type": "text",
            "name": "username",
            "placeholder": "Enter your username",
            "maxlength": "30",
            "required": "true",
            "autocomplete": "off"
        }
    )
    print(repr(new_input_node))
    print(new_input_node.to_html())
    new_parent_node = ParentNode("div", [new_leaf_node, new_text_node, new_input_node], props={"id": "main"})
    print(repr(new_parent_node))



if __name__ == "__main__":
    main()
