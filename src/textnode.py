from enum import Enum

from leafnode import LeafNode


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if not isinstance(other, TextNode):
            return False
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self):
        return f"{self.text} {self.text_type} {self.url}"


def text_node_to_html(text_node):
    if text_node.text_type == TextType.TEXT.value:
        return LeafNode(None, text_node.text)
    elif text_node.text_type == TextType.BOLD.value:
        return LeafNode("b", text_node.text)
    elif text_node.text_type == TextType.ITALIC.value:
        return LeafNode("i", text_node.text)
    elif text_node.text_type == TextType.CODE.value:
        return LeafNode("code", text_node.text)
    elif text_node.text_type == TextType.LINK.value:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    elif text_node.text_type == TextType.IMAGE.value:
        return LeafNode(
            "i", text_node.text, {"alt": text_node.text, "src": text_node.url}
        )
    else:
        raise ValueError(f"Invalid text type: {text_node.text_type}")
