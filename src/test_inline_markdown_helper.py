import unittest

from inline_text_helper import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_text_nodes,
)
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
                TextType.TEXT.value,
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
                TextType.TEXT.value,
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
            TextType.TEXT.value,
        )

        text_2 = TextNode(
            "`This is text with a code section`",
            TextType.TEXT.value,
        )

        nodes = [text_1, text_2]

        new_nodes = split_nodes_delimiter(nodes, "`", TextType.CODE.value)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with one code section", TextType.CODE.value),
                TextNode(" and some text", TextType.TEXT.value),
                TextNode("This is text with a code section", TextType.CODE.value),
            ],
        )

    def test_extract_single_image(self):
        extracted_images = extract_markdown_images(
            "![alt text](https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png)"
        )

        self.assertEqual(
            extracted_images,
            [
                (
                    "alt text",
                    "https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png",
                )
            ],
        )

    def test_extract_multi_image(self):
        extracted_images = extract_markdown_images(
            "![alt text](https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png) and ![another](https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png)"
        )

        self.assertEqual(
            extracted_images,
            [
                (
                    "alt text",
                    "https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png",
                ),
                (
                    "another",
                    "https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png",
                ),
            ],
        )

    def test_extract_single_image_link(self):
        extracted_images = extract_markdown_images(
            "[alt text](https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png)"
        )

        self.assertEqual(
            extracted_images,
            [],
        )

    def test_extract_single_link(self):
        extracted_images = extract_markdown_links(
            "[link](https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png)"
        )

        self.assertEqual(
            extracted_images,
            [
                (
                    "link",
                    "https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png",
                ),
            ],
        )

    def test_extract_multi_link(self):
        extracted_images = extract_markdown_links(
            "[link](https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png) and [another link](https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png)"
        )

        self.assertEqual(
            extracted_images,
            [
                (
                    "link",
                    "https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png",
                ),
                (
                    "another link",
                    "https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png",
                ),
            ],
        )

    def test_split_node_double_image(self):
        markdown_image = [
            TextNode(
                "This is an image ![alt text](https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png)",
                TextType.TEXT.value,
            )
        ]
        new_nodes = split_nodes_image(markdown_image)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is an image ", TextType.TEXT.value),
                TextNode(
                    "alt text",
                    TextType.IMAGE.value,
                    "https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png",
                ),
            ],
        )

    def test_split_node_images(self):
        markdown_image = [
            TextNode(
                "This is an image ![alt text](https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png) and ![another](https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png) This is the end of the text",
                TextType.TEXT.value,
            )
        ]
        new_nodes = split_nodes_image(markdown_image)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is an image ", TextType.TEXT.value),
                TextNode(
                    "alt text",
                    TextType.IMAGE.value,
                    "https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png",
                ),
                TextNode(" and ", TextType.TEXT.value),
                TextNode(
                    "another",
                    TextType.IMAGE.value,
                    "https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png",
                ),
                TextNode(" This is the end of the text", TextType.TEXT.value),
            ],
        )

    def test_split_node_image_no_empty_strings(self):
        markdown_image = [
            TextNode(
                "![alt text](https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png) and ![another](https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png)",
                TextType.TEXT.value,
            )
        ]
        new_nodes = split_nodes_image(markdown_image)
        self.assertEqual(
            new_nodes,
            [
                TextNode(
                    "alt text",
                    TextType.IMAGE.value,
                    "https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png",
                ),
                TextNode(" and ", TextType.TEXT.value),
                TextNode(
                    "another",
                    TextType.IMAGE.value,
                    "https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png",
                ),
            ],
        )

    def test_split_node_link(self):
        markdown_link = [
            TextNode(
                "[link](https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png)",
                TextType.TEXT.value,
            )
        ]
        new_nodes = split_nodes_link(markdown_link)
        self.assertEqual(
            new_nodes,
            [
                TextNode(
                    "link",
                    TextType.LINK.value,
                    "https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png",
                ),
            ],
        )

    def test_text_to_text_nodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)"
        nodes = text_to_text_nodes(text)
        self.assertEqual(
            nodes,
            [
                TextNode("This is ", TextType.TEXT.value),
                TextNode("text", TextType.BOLD.value),
                TextNode(" with an ", TextType.TEXT.value),
                TextNode("italic", TextType.ITALIC.value),
                TextNode(" word and a ", TextType.TEXT.value),
                TextNode("code block", TextType.CODE.value),
                TextNode(" and an ", TextType.TEXT.value),
                TextNode(
                    "image", TextType.IMAGE.value, "https://i.imgur.com/zjjcJKZ.png"
                ),
                TextNode(" and a ", TextType.TEXT.value),
                TextNode("link", TextType.LINK.value, "https://boot.dev"),
            ],
        )


if __name__ == "__main__":
    unittest.main()
