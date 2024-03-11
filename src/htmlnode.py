class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = props
        self.props = children

    def __repr__(self):
        return f"<{self.tag} {self.props_to_html()}>{self.value}</{self.tag}>"

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        if self.props:
            return f"href={self.props.get('href')} target={self.props.get('target')}"
