from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if not isinstance(node, TextNode):
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
