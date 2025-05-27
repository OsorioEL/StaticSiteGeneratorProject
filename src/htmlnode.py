


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
        return(f"HTMLNode({self.tag},{self.value},{self.children},{self.props})")