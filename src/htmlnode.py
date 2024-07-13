from enum import Enum


class HtmlNodeTag(Enum):
    DIV = "div"
    BOLD = "b"
    ITALIC = "i"
    CODE = "code"
    HYPER_LINK = "a"
    IMAGE = "img"
    HEADING_1 = "h1"
    HEADING_2 = "h2"
    HEADING_3 = "h3"
    HEADING_4 = "h4"
    HEADING_5 = "h5"
    HEADING_6 = "h6"
    PARAGRAPH = "p"
    LIST_ITEM = "li"
    ORDERED_LIST = "ol"
    UNORDERED_LIST = "ul"
    QUOTE = "blockquote"
    PRE_FORMATTED_TEXT = "pre"


class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self):
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __eq__(self, other):
        return (
            self.tag == other.tag
            and self.value == other.value
            and self.children == other.children
            and self.props == other.props
        )

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        if self.props:
            prop_str = " ".join(
                [f"{prop_name}={self.props[prop_name]}" for prop_name in self.props]
            )
            return " " + prop_str

        return ""
