import unittest

from textnode import TextNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold", "http://www.google.com")
        node2 = TextNode("This is a text node", "bold", "http://www.google.com")
        self.assertEqual(node, node2)

    def test_repr(self):
        self.assertEqual(
            f"{TextNode('This is a text node', 'bold', 'http://www.google.com')}",
            "This is a text node bold http://www.google.com",
        )


if __name__ == "__main__":
    unittest.main()
