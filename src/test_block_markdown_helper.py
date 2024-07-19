import unittest

from block_markdown_helper import (
    check_if_code,
    check_if_heading,
    check_if_ordered_list,
    check_if_quote,
    check_if_unordered_list,
    extract_title,
    markdown_to_blocks,
    markdown_to_html_node,
)


class TestMarkdownToHTML(unittest.TestCase):
    def test_markdown_to_block_with_quote(self):
        md = """ 
This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

> This is a list
> with items
        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "> This is a list\n> with items",
            ],
        )

    def test_markdown_to_block(self):
        md = """ 
This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )

    def test_markdown_to_block_redundant_lines(self):
        md = """ 
This is **bolded** paragraph





This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )

    def test_check_if_heading_true(self):
        md = "## this is a heading"
        self.assertTrue(check_if_heading(md))

    def test_check_if_heading_false(self):
        md = "# this is a heading"
        self.assertTrue(check_if_heading(md))

    def test_check_if_heading_max_hash(self):
        md = "###### this is a heading"
        self.assertTrue(check_if_heading(md))

    def test_check_if_heading_rejects_more_than_6_hash(self):
        md = "####### this is a not heading"
        self.assertFalse(check_if_heading(md))

    def test_check_if_quote_true(self):
        md = "> this\n> is\n> a quote"
        self.assertTrue(check_if_quote(md))

    def test_check_if_quote_false(self):
        md = "> this is\n? not\n> a quote"
        self.assertFalse(check_if_quote(md))

    def test_check_if_unordered_list_true(self):
        md = "* this\n* is\n* a unordered list"
        self.assertTrue(check_if_unordered_list(md))

    def test_check_if_unordered_list_true_dash(self):
        md = "- this\n- is\n- a unordered list"
        self.assertTrue(check_if_unordered_list(md))

    def test_check_if_unordered_list_mixed_start(self):
        md = "- this is\n* not\n- a unordered list"
        self.assertFalse(check_if_unordered_list(md))

    def test_check_if_ordered_list_true(self):
        md = "1. this\n2. is\n3. a ordered list"
        self.assertTrue(check_if_ordered_list(md))

    def test_check_if_ordered_list_false(self):
        md = "1. this is\n2. not\n4. a unordered list"
        self.assertFalse(check_if_ordered_list(md))

    def test_check_if_code_true(self):
        md = "```\nthis is a block of code\n```"
        self.assertTrue(check_if_code(md))

    def test_check_if_code_false(self):
        md = "``` ```"
        self.assertFalse(check_if_code(md))

    # def test_markdown_to_html_heading(self):
    #     heading_md = "## this is a heading"
    #
    #     heading_html_node = markdown_to_html(heading_md)
    #
    #     self.assertEqual(heading_html_node.to_html(), "<h2>this is a heading</h2>")

    # def test_markdown_to_html_paragraph(self):
    #     heading_md = "####### this not a heading but a paragraph"
    #
    #     self.assertEqual(
    #         markdown_to_html(heading_md).to_html(),
    #         "<p>####### this not a heading but a paragraph</p>",
    #     )
    #
    # def test_markdown_to_html_ordered_list(self):
    #     ordered_list_md = "1. this\n2. is\n3. a ordered list"
    #     self.assertEqual(
    #         markdown_to_html(ordered_list_md).to_html(),
    #         "<ol><li>this</li><li>is</li><li>a ordered list</li></ol>",
    #     )
    #
    # def test_markdown_to_html_unordered_list(self):
    #     unordered_list_md = "* this\n* is\n* a unordered list"
    #     self.assertEqual(
    #         markdown_to_html(unordered_list_md).to_html(),
    #         "<ul><li>this</li><li>is</li><li>a unordered list</li></ul>",
    #     )
    #
    # def test_markdown_to_html_quote(self):
    #     quote_md = "> this\n> is\n> a quote"
    #     self.assertEqual(
    #         markdown_to_html(quote_md).to_html(),
    #         "<blockquote>this is a quote</blockquote>",
    #     )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

    """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )

    def test_extract_titile(self):
        md = """
# this is a title

 extra text
            """

        self.assertEqual(extract_title(md), "this is a title")

    def test_extract_tile_no_heading(self):
        md = """
this contains no h1 heading
            """

        with self.assertRaises(ValueError):
            extract_title(md)


if __name__ == "__main__":
    unittest.main()
