import unittest

from textnode import TextNode, text_node_to_html


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold", "http://www.google.com")
        node2 = TextNode("This is a text node", "bold", "http://www.google.com")
        self.assertEqual(node, node2)


if __name__ == "__main__":
    unittest.main()
