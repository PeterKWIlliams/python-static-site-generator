from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if not self.value:
            raise ValueError("All leaf node require a value")
        if not self.tag:
            return self.value
        leaf_html = f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        return leaf_html

    def props_to_html(self):
        if self.props:
            prop_str = " ".join(
                [f"{prop_name}={self.props[prop_name]}" for prop_name in self.props]
            )
            return " " + prop_str

        return ""
