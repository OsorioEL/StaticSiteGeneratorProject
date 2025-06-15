from htmlnode import ParentNode, LeafNode
from textnode import text_to_textnodes, text_node_to_html_node
from textnode import TextNode, TextType
from textnode import markdown_to_blocks, block_to_block_type, BlockType

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(node) for node in text_nodes]

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []

    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type == BlockType.PARAGRAPH:
            normalized = block.replace("\n", " ")
            children.append(ParentNode("p", text_to_children(normalized)))

        elif block_type == BlockType.HEADING:
            heading_level = len(block.split(" ")[0])
            content = block[heading_level+1:].strip()
            children.append(ParentNode(f"h{heading_level}", text_to_children(content)))

        elif block_type == BlockType.CODE:
            lines = block.splitlines()

            # Handle both:
            # ```
            # code lines
            # ```
            # and single-line cases (defensive fallback)
            if lines and lines[0].startswith("```"):
                # Remove the first and last line if both are ```
                if len(lines) >= 2 and lines[-1].startswith("```"):
                    code_content = "\n".join(lines[1:-1])
                else:
                    code_content = "\n".join(lines[1:])
            else:
                # If no proper fencing, take as-is
                code_content = block

            if code_content.strip() == "":
                raise ValueError("Code block has no content")

            code_node = LeafNode("code", code_content)
            children.append(ParentNode("pre", [code_node]))


        elif block_type == BlockType.QUOTE:
            # remove leading > or >'s with optional space
            quote_text = "\n".join([line.lstrip("> ").strip() for line in block.splitlines()])
            children.append(ParentNode("blockquote", text_to_children(quote_text)))

        elif block_type == BlockType.UNORDERED_LIST:
            lines = block.splitlines()
            list_items = [ParentNode("li", text_to_children(line.lstrip("-* ").strip())) for line in lines]
            children.append(ParentNode("ul", list_items))

        elif block_type == BlockType.ORDERED_LIST:
            lines = block.splitlines()
            list_items = [ParentNode("li", text_to_children(re.sub(r"^\d+\.\s*", "", line))) for line in lines]
            children.append(ParentNode("ol", list_items))

    return ParentNode("div", children)
