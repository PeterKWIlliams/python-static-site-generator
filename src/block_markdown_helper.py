from enum import Enum

from htmlnode import HTMLNode
from parentnode import ParentNode


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown_block):
    markdown = markdown_block.split("\n\n")
    new_markdown = []
    for line in markdown:
        if line == "":
            continue
        new_markdown.append(line.strip())
    return new_markdown


def check_if_heading(markdown_block):
    is_heading = False

    if markdown_block.startswith("#"):
        start = "#"
        for i in range(1, 7):
            if markdown_block.startswith(start + " "):
                is_heading = True
                break
            elif markdown_block.startswith(start + "#"):
                start += "#"
            else:
                break
    return is_heading


def check_if_code(markdown_block):
    markdown_lines = markdown_block.split("\n")
    if (
        len(markdown_lines) >= 2
        and markdown_block.startswith("```")
        and markdown_block.endswith("```")
    ):
        return True
    else:
        return False


def check_if_quote(markdown_block):
    is_quote = False
    if markdown_block.startswith(">"):
        is_quote = True
        markdown_lines = markdown_block.split("\n")
        for line in markdown_lines:
            if line.startswith(">"):
                continue
            else:
                is_quote = False
                break
    return is_quote


def check_if_unordered_list(markdown_block):
    is_unordered_list = False
    if markdown_block.startswith("* ") or markdown_block.startswith("- "):
        markdown_lines = markdown_block.split("\n")
        first_character = markdown_lines[0][0]
        for line in markdown_lines:
            if line.startswith(first_character):
                is_unordered_list = True
            else:
                is_unordered_list = False
                break
    return is_unordered_list


def check_if_ordered_list(markdown_block):
    is_ordered_list = False
    start = 1
    if markdown_block.startswith(f"{start}. "):
        is_ordered_list = True
        markdown_lines = markdown_block.split("\n")
        for line in markdown_lines:
            if line.startswith(f"{start}. "):
                start += 1
            else:
                is_ordered_list = False
                break
    return is_ordered_list


def block_to_block_type(markdown_block):
    if check_if_heading(markdown_block):
        return BlockType.HEADING.value
    elif check_if_code(markdown_block):
        return BlockType.CODE.value
    elif check_if_quote(markdown_block):
        return BlockType.QUOTE.value
    elif check_if_unordered_list(markdown_block):
        return BlockType.UNORDERED_LIST.value
    elif check_if_ordered_list(markdown_block):
        return BlockType.ORDERED_LIST.value
    else:
        return BlockType.PARAGRAPH.value
