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
