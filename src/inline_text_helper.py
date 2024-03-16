import re

from textnode import TextNode, TextType


def text_to_text_nodes(text):
    text_nodes = [TextNode(text, TextType.TEXT.value)]
    delimiters = {
        "**": TextType.BOLD.value,
        "*": TextType.ITALIC.value,
        "`": TextType.CODE.value,
    }
    for delimiter in delimiters:
        text_nodes = split_nodes_delimiter(text_nodes, delimiter, delimiters[delimiter])
    text_nodes = split_nodes_image(text_nodes)
    text_nodes = split_nodes_link(text_nodes)
    return text_nodes


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT.value:
            new_nodes.append(node)
            continue
        text_nodes = []
        word_list = node.text.split(delimiter)
        for index, word in enumerate(word_list):
            if len(word_list) % 2 == 0:
                raise ValueError("Not valid markdown")
            if word == "":
                continue
            if index % 2 == 0:
                text_nodes.append(TextNode(word, TextType.TEXT.value))
            else:
                text_nodes.append(TextNode(word, text_type))
        new_nodes.extend(text_nodes)
    return new_nodes


def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)


def split_nodes_image(old_nodes):
    new_node_list = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT.value:
            new_node_list.append(node)
            continue
        image_tuples = extract_markdown_images(node.text)
        if len(image_tuples) == 0:
            new_node_list.append(node)
            continue
        after_split = ""
        for index in range(0, len(image_tuples)):
            if after_split == "":
                split_text = node.text.split(
                    f"![{image_tuples[index][0]}]({image_tuples[index][1]})", 1
                )
            else:
                split_text = after_split.split(
                    f"![{image_tuples[index][0]}]({image_tuples[index][1]})", 1
                )
                if len(split_text) != 2:
                    raise ValueError("Not valid markdown")
            if split_text[0] != "":
                new_node_list.append(TextNode(split_text[0], TextType.TEXT.value))
            new_node_list.append(
                TextNode(
                    image_tuples[index][0], TextType.IMAGE.value, image_tuples[index][1]
                )
            )

            after_split = split_text[1]
            if index == len(image_tuples) - 1 and after_split != "":
                new_node_list.append(TextNode(after_split, TextType.TEXT.value))

    return new_node_list


def extract_markdown_links(text):
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)


def split_nodes_link(old_nodes):
    new_node_list = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT.value:
            new_node_list.append(node)
            continue
        link_tuples = extract_markdown_links(node.text)

        if len(link_tuples) == 0:
            new_node_list.append(node)
            continue
        after_split = None
        for index in range(0, len(link_tuples)):
            if after_split == None:
                split_text = node.text.split(
                    f"[{link_tuples[index][0]}]({link_tuples[index][1]})", 1
                )
            else:
                split_text = after_split.split(
                    f"[{link_tuples[index][0]}]({link_tuples[index][1]})", 1
                )
            if split_text[0] != "":
                new_node_list.append(TextNode(split_text[0], TextType.TEXT.value))
            new_node_list.append(
                TextNode(
                    link_tuples[index][0], TextType.LINK.value, link_tuples[index][1]
                )
            )

            after_split = split_text[1]
            if index == len(link_tuples) - 1 and after_split != "":
                new_node_list.append(TextNode(after_split, TextType.TEXT.value))

    return new_node_list
