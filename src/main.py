from htmlnode import HTMLNode
from leafnode import LeafNode
from textnode import TextNode


def main():
    textnode = TextNode("This is the text node", "bold")
    print(textnode.__repr__)
    htmlnode = HTMLNode("div", "hello", None, {"target": "hello", "href": "hello"})
    print(htmlnode.__repr__)
    leafnode = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
    print(leafnode.__repr__)


main()
