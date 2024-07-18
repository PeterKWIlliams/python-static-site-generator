import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_eq(self):
        node1 = LeafNode(
            "div",
            "Hello there!",
            props={"target": "_blank", "href": "https://www.google.com"},
        )
        node2 = LeafNode(
            "div",
            "Hello there!",
            props={"target": "_blank", "href": "https://www.google.com"},
        )
        self.assertEqual(node1, node2)

    def test_eq_false(self):
        node1 = LeafNode(
            "div",
            "Hello there!",
            props={"target": "_blank", "href": "https://www.google.com"},
        )
        node2 = LeafNode(
            "div",
            "Not Hello there!",
            props={"target": "_blank", "href": "https://www.boogle.com"},
        )
        self.assertNotEqual(node1, node2)

    def test_repr(self):
        node1 = LeafNode("div", "Hello there!")
        self.assertEqual(repr(node1), "<div>Hello there!</div>")

    def test_to_html(self):
        node1 = LeafNode(
            "div",
            "Hello there!",
            props={"target": "_blank", "href": "https://www.google.com"},
        )

        self.assertEqual(
            node1.to_html(),
            '<div target="_blank" href="https://www.google.com">Hello there!</div>',
        )

    def test_to_html_no_tag(self):
        node1 = LeafNode(
            None,
            "Hello there!",
        )

        self.assertEqual(
            node1.to_html(),
            "Hello there!",
        )

    def test_props_to_html(self):
        node1 = LeafNode(
            "div",
            "Hello there!",
            props={"target": "_blank", "href": "https://www.google.com"},
        )

        self.assertEqual(
            node1.props_to_html(), ' target="_blank" href="https://www.google.com"'
        )


if __name__ == "__main__":
    unittest.main()
