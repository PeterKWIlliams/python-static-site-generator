import unittest

from leafnode import LeafNode
from parentnode import ParentNode


class TestParentNode(unittest.TestCase):
    def test_to_html_many_children(self):
        leafNode1 = LeafNode("p", "Hello World")
        leafNode2 = LeafNode(
            "a",
            "Click me",
            props={"target": "_blank", "href": "https://www.google.com"},
        )
        parent_node1 = ParentNode(
            "div",
            [leafNode1, leafNode2],
            props={"target": "_blank"},
        )

        self.assertEqual(
            parent_node1.to_html(),
            '<div target="_blank"><p>Hello World</p><a target="_blank" href="https://www.google.com">Click me</a></div>',
        )

    def test_to_html_single_child(self):
        leafNode1 = LeafNode("p", "Hello World")
        parent_node1 = ParentNode(
            "div",
            [leafNode1],
            props={"target": "_blank"},
        )

        self.assertEqual(
            parent_node1.to_html(),
            '<div target="_blank"><p>Hello World</p></div>',
        )

    def test_to_html_nested_parent(self):
        leafNode1 = LeafNode("p", "Hello World")
        parent_node1 = ParentNode(
            "div",
            [leafNode1],
            props={"target": "_blank"},
        )
        parent_node2 = ParentNode(
            "div",
            [parent_node1],
            props={"target": "_blank"},
        )

        self.assertEqual(
            parent_node2.to_html(),
            '<div target="_blank"><div target="_blank"><p>Hello World</p></div></div>',
        )


if __name__ == "__main__":
    unittest.main()
