import unittest

from block_markdown_helper import (
    check_if_code,
    check_if_heading,
    check_if_ordered_list,
    check_if_quote,
    check_if_unordered_list,
    markdown_to_blocks,
)


class TestMarkdownToHTML(unittest.TestCase):
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

    def test_check_if_quote_False(self):
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

    def test_check_if_ordered_list_false(self):
        md = "``` this is\na\nblock of code\n```"
        self.assertTrue(check_if_code(md))

    def test_check_if_code_false(self):
        md = "``` ```"
        self.assertFalse(check_if_code(md))


if __name__ == "__main__":
    unittest.main()
