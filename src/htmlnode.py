from textnode import *


def text_node_to_html_node(text_node:TextNode):
    if text_node.text_type not in TextType:
        raise TypeError("Invalid text type")
    if text_node.text_type == TextType.PLAIN or text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    if text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    if text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    if text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    if text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    if text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})


class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children or []
        self.props = props or {}

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if self.props:
            serialized_props = " "
            for key, value in self.props.items():
                if value is None or value == "": ## Boolean props
                    serialized_props += f'{key} '
                else:
                    serialized_props += f'{key}="{value}" '
            return serialized_props.rstrip()
        return ""

    def __repr__(self):
        return f"Tag: {self.tag}, Value: {self.value}, Children: {self.children}, Props: {self.props}"

    def __eq__(self, other):
        return (self.tag == other.tag and
                self.value == other.value and
                self.children == other.children and
                self.props == other.props)


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if not self.value:
            raise ValueError("Value cannot be empty")
        if not self.tag:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag, children:list[HTMLNode], props = None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("Tag cannot be empty")
        if not self.children:
            raise ValueError("This is a parent node, has to have children")
        node_string = f"<{self.tag}{self.props_to_html()}>"
        for child in self.children:
            node_string += child.to_html()
        node_string += f"</{self.tag}>"
        return node_string
