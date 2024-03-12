import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode(
            "div",
            "Hello there!",
            props={"target": "_blank", "href": "https://www.google.com"},
        )
        node2 = HTMLNode(
            "div",
            "Hello there!",
            props={"target": "_blank", "href": "https://www.google.com"},
        )
        self.assertEqual(node, node2)

    def test_repr(self):
        self.assertEqual(
            f"{HTMLNode('div', 'Hello there!')}", "<div>Hello there!</div>"
        )


if __name__ == "__main__":
    unittest.main()
