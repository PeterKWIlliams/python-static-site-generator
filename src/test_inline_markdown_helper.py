import unittest

from inline_text_helper import split_nodes_delimiter
from leafnode import LeafNode
from textnode import TextNode, TextType


class TestInlineTextHelper(unittest.TestCase):
    def test_delim_single_bold(self):
        text_1 = [
            TextNode("**This is text with one bolded section**", TextType.TEXT.value)
        ]

        new_node = split_nodes_delimiter(text_1, "**", TextType.BOLD.value)
        self.assertEqual(
            new_node,
            [
                TextNode("This is text with one bolded section", TextType.BOLD.value),
            ],
        )

    def test_delim_single_bold_fail(self):
        text_1 = [
            TextNode("*This is text with one bolded section**", TextType.TEXT.value)
        ]

        with self.assertRaises(ValueError):
            split_nodes_delimiter(text_1, "**", TextType.BOLD.value)

    def test_delim_multi_bold(self):
        text_1 = [
            TextNode(
                "**This is text with three** **bolded****sections**",
                TextType.TEXT.value,
            )
        ]

        new_node = split_nodes_delimiter(text_1, "**", TextType.BOLD.value)
        self.assertEqual(
            new_node,
            [
                TextNode("This is text with three", TextType.BOLD.value),
                TextNode(" ", TextType.TEXT.value),
                TextNode("bolded", TextType.BOLD.value),
                TextNode("sections", TextType.BOLD.value),
            ],
        )

    def test_delim_single_code(self):
        text_1 = [
            TextNode(
                "`This is text with one code section` and some text",
                TextType.CODE.value,
            )
        ]

        new_node = split_nodes_delimiter(text_1, "`", TextType.CODE.value)
        self.assertEqual(
            new_node,
            [
                TextNode("This is text with one code section", TextType.CODE.value),
                TextNode(" and some text", TextType.TEXT.value),
            ],
        )

    def test_delim_single_italic(self):
        text_1 = [
            TextNode(
                " *This is text with one italic section* with text and empty space at start",
                TextType.ITALIC.value,
            )
        ]

        new_node = split_nodes_delimiter(text_1, "*", TextType.ITALIC.value)
        self.assertEqual(
            new_node,
            [
                TextNode(" ", TextType.TEXT.value),
                TextNode("This is text with one italic section", TextType.ITALIC.value),
                TextNode(" with text and empty space at start", TextType.TEXT.value),
            ],
        )

    def test_delim_multi_node(self):
        text_1 = TextNode(
            "`This is text with one code section` and some text",
            TextType.CODE.value,
        )

        text_2 = TextNode(
            "`This is text with a code section`",
            TextType.CODE.value,
        )

        leaf_node = LeafNode(
            "b",
            "Im some bold text",
        )

        nodes = [text_1, text_2, leaf_node]

        new_nodes = split_nodes_delimiter(nodes, "`", TextType.CODE.value)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with one code section", TextType.CODE.value),
                TextNode(" and some text", TextType.TEXT.value),
                TextNode("This is text with a code section", TextType.CODE.value),
                LeafNode("b", "Im some bold text"),
            ],
        )


if __name__ == "__main__":
    unittest.main()
