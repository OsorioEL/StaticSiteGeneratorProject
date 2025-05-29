


class HTMLNode:
    def __init__(self,tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("Child classes will override this mehod to render themselves as HTML")

    def props_to_html(self):
        if not self.props:
            return ""
        props_string=" ".join(map(lambda kv: f'{kv[0]}="{kv[1]}"',self.props.items()))
        return props_string

    def __repr__(self):
        if type(self) is HTMLNode:
            return f"HTMLNode({self.tag},{self.value},{self.children},{self.props})"
        elif type(self) is LeafNode:
            return(f"LeafNode({self.tag},{self.value},{self.children},{self.props})")
        else:
            return(f"ParentNode({self.tag},{self.children},{self.props})")
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, props=props)
        if value is None and tag is None:
            raise ValueError("All leaf nodes must have a value")
        
    def to_html(self):
        if self is None:
            raise ValueError("All leaf nodes must have a value")
        if self.tag is None:
            # if no tag, return value directly as raw text
            return str(self.value)
        else:
            props_html = self.props_to_html()
            if props_html:
                return f"<{self.tag} {props_html}>{self.value}</{self.tag}>"
            else:
                return f"<{self.tag}>{self.value}</{self.tag}>"
        
        
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props)
        
    def to_html(self):
        if self.tag is None:
            raise ValueError("Parent nodes must have a tag")
        elif not self.children:
            raise ValueError("Parent nodes must have children")
        else:
            if self.props:
                props_html = self.props_to_html()
                children_html = "".join(child.to_html() for child in self.children)
                return f"<{self.tag} {props_html}>{children_html}</{self.tag}>"
            else:
                children_html = "".join(child.to_html() for child in self.children)
                return f"<{self.tag}>{children_html}</{self.tag}>"