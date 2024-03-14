from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("All parent nodes require a value")
        if not self.children:
            raise ValueError("All parent nodes require children")

        child_html = "".join([child.to_html() for child in self.children])
        parent_html = f"<{self.tag}{self.props_to_html()}>{child_html}</{self.tag}>"
        return parent_html

    def props_to_html(self):
        if self.props:
            prop_str = " ".join(
                [f"{prop_name}={self.props[prop_name]}" for prop_name in self.props]
            )
            return " " + prop_str

        return ""
