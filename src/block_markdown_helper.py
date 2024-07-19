from enum import Enum

from htmlnode import HtmlNodeTag
from inline_markdown_helper import text_to_text_nodes
from leafnode import LeafNode
from parentnode import ParentNode
from textnode import text_node_to_html


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if block.startswith("# "):
            return block[2:]
    raise ValueError("No title found")


def markdown_to_blocks(markdown_block):
    blocks = markdown_block.split("\n\n")
    new_markdown = []
    for block in blocks:
        if block.strip() == "":
            continue
        block = block.strip()
        new_markdown.append(block)
    return new_markdown


def markdown_to_html_node(markdown):
    markdown_blocks = markdown_to_blocks(markdown)
    print(markdown_blocks)
    html_nodes = []

    for block in markdown_blocks:
        html_nodes.append(markdown_to_html(block))

    return ParentNode(HtmlNodeTag.DIV.value, html_nodes)


def markdown_to_html(markdown_block):
    block_type = block_to_block_type(markdown_block)

    if block_type == BlockType.HEADING.value:
        return heading_block_to_html(markdown_block)
    if block_type == BlockType.CODE.value:
        return code_block_to_html(markdown_block)
    if block_type == BlockType.QUOTE.value:
        return quote_block_to_html(markdown_block)
    if block_type == BlockType.UNORDERED_LIST.value:
        return unordered_list_to_html(markdown_block)
    if block_type == BlockType.ORDERED_LIST.value:
        return ordered_list_to_html(markdown_block)
    if block_type == BlockType.PARAGRAPH.value:
        return paragraph_block_to_html(markdown_block)

    raise ValueError("Not a valid block type")


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
            if line.strip().startswith(">"):
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
    if check_if_code(markdown_block):
        return BlockType.CODE.value
    if check_if_quote(markdown_block):
        return BlockType.QUOTE.value
    if check_if_unordered_list(markdown_block):
        return BlockType.UNORDERED_LIST.value
    if check_if_ordered_list(markdown_block):
        return BlockType.ORDERED_LIST.value

    return BlockType.PARAGRAPH.value


def text_to_children(text):
    text_nodes = text_to_text_nodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html(text_node)
        children.append(html_node)
    return children


def quote_block_to_html(markdown_block):

    markdown_lines = markdown_block.split("\n")
    new_lines = []

    for line in markdown_lines:
        if not line.startswith(">"):
            raise ValueError("Not a quote block")
        new_lines.append(line.lstrip(">").strip())

    quote_block = " ".join(new_lines)
    children = text_to_children(quote_block)
    return ParentNode(HtmlNodeTag.QUOTE.value, children)


def code_block_to_html(markdown_block):
    if not markdown_block.startswith("```"):
        raise ValueError("Not a code block")
    code_block = markdown_block[4:-3]
    children = text_to_children(code_block)
    code = ParentNode(HtmlNodeTag.CODE.value, children)
    return ParentNode(
        HtmlNodeTag.PRE_FORMATTED_TEXT.value,
        [code],
    )


def ordered_list_to_html(markdown_block):
    markdown_lines = markdown_block.split("\n")
    list_items = []

    for line in markdown_lines:
        children = text_to_children(line[3:])
        list_items.append(ParentNode(HtmlNodeTag.LIST_ITEM.value, children))

    return ParentNode(HtmlNodeTag.ORDERED_LIST.value, list_items)


def unordered_list_to_html(markdown_block):
    markdown_lines = markdown_block.split("\n")
    list_items = []
    for line in markdown_lines:
        children = text_to_children(line[2:])
        list_items.append(ParentNode(HtmlNodeTag.LIST_ITEM.value, children))

    return ParentNode(HtmlNodeTag.UNORDERED_LIST.value, list_items)


def heading_block_to_html(markdown_block):
    count = 0
    for char in markdown_block:
        if char == "#":
            count += 1
        else:
            break

    heading_block = markdown_block[count + 1 :]

    children = text_to_children(heading_block)
    heading_value = f"HEADING_{count}"
    return ParentNode(getattr(HtmlNodeTag, heading_value).value, children)


def paragraph_block_to_html(markdown_block):
    lines = markdown_block.split("\n")
    paragraph_block = " ".join(lines)
    children = text_to_children(paragraph_block)
    return ParentNode(HtmlNodeTag.PARAGRAPH.value, children)
