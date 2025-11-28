from textnode import *
import re

def split_nodes_delimiter(old_nodes:list[TextNode], delimiter:str, text_type:TextType):
    new_nodes = []

    if delimiter not in text_type_delimiters.values() or delimiter == "":
        raise ValueError("Invalid delimiter")

    for node in old_nodes:
        to_be_nodes = []
        if node.text_type not in [TextType.TEXT, TextType.PLAIN] or delimiter not in node.text:
            new_nodes.append(node)
            continue

        if node.text.count(delimiter)%2 != 0:
            raise ValueError(f"Delimiter {delimiter} lacks a pair, string: '{node.text}' node type: {node.text_type}")
        to_be_nodes.extend(node.text.split(delimiter))

        for i in range(0, len(to_be_nodes)):
            if len(to_be_nodes[i])<1:
                continue
            if i%2 != 0: #the cycle has to be indented, otherwise this line won't work properly
                new_nodes.append(TextNode(to_be_nodes[i], text_type))
            else:
                new_nodes.append(TextNode(to_be_nodes[i], TextType.TEXT))
    return new_nodes

def extract_markdown_images(text:str):
    matches = re.findall(r"!\[(.+?)\]\((.+?)\)", text)
    return matches

def extract_markdown_links(text:str):
    matches = re.findall(r"(?<!\!)\[(.+?)\]\((.+?)\)", text)
    return matches

def split_nodes_image(nodes:list[TextNode]):
    new_nodes = []

    for node in nodes:
        if node.text_type not in [TextType.TEXT, TextType.PLAIN]:
            new_nodes.append(node)
            continue
        images = extract_markdown_images(node.text)
        if images:
            alt_text, img_url = images[0]
            text_strings = node.text.split(f"![{alt_text}]({img_url})", 1)
            if text_strings[0]:
                new_nodes.append(TextNode(text_strings[0], TextType.TEXT))
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, img_url))
            if text_strings[1]:
                new_nodes.extend(split_nodes_image([TextNode(text_strings[1], TextType.TEXT)]))
        else:
            new_nodes.append(node)
    return new_nodes

def split_nodes_link(nodes:list[TextNode]):
    new_nodes = []

    for node in nodes:
        if node.text_type not in [TextType.TEXT, TextType.PLAIN]:
            new_nodes.append(node)
            continue
        links = extract_markdown_links(node.text)
        if links:
            link_text, url = links[0]
            text_strings = node.text.split(f"[{link_text}]({url})", 1)
            if text_strings[0]:
                new_nodes.append(TextNode(text_strings[0], TextType.TEXT))
            new_nodes.append(TextNode(link_text, TextType.LINK, url))
            if text_strings[1]:
                new_nodes.extend(split_nodes_link([TextNode(text_strings[1], TextType.TEXT)]))
        else:
            new_nodes.append(node)
    return new_nodes

#crackpipe regex implementation of the functions above, i can't comprehend those regexes at this point so i am afraid they may break in unexpected ways
"""
def split_nodes_image(nodes:list[TextNode]):
    new_nodes = []

    for node in nodes:
        if node.text_type not in [TextType.TEXT, TextType.PLAIN]:
            new_nodes.append(node)
            continue
        matches:list[tuple[str, str, str]] = re.findall(r"!\[(.+?)\]\((.+?)\)|((?:(?!!\[(?:.+?)\]\((?:.+?)\)).)+)", node.text)
        for alt_text, img_url, text in matches:
            if text:
                new_nodes.append(TextNode(text, TextType.TEXT))
            else:
                new_nodes.append(TextNode(alt_text, TextType.IMAGE, img_url))
    return new_nodes

def split_nodes_link(nodes:list[TextNode]):
    new_nodes = []

    for node in nodes:
        if node.text_type not in [TextType.TEXT, TextType.PLAIN]:
            new_nodes.append(node)
            continue
        to_be_nodes: list[tuple[str, str, str]] = re.findall(r"(?:(?<!\!)\[([^\]]+?)\]\(([^)]+?)\))|((?:.|\n)+?)(?=(?<!\!)\[|$)", node.text)
        for text, url, other in to_be_nodes:
            if text and url:
                new_nodes.append(TextNode(text, TextType.LINK, url))
            else:
                new_nodes.append(TextNode(other, TextType.TEXT))

    return new_nodes
"""

def text_to_textnodes(text:str):
    text = TextNode(text, TextType.TEXT)
    nodes = split_nodes_image([text])
    nodes = split_nodes_link(nodes)
    for text_type in text_type_delimiters.keys():
        nodes = split_nodes_delimiter(nodes, text_type_delimiters[text_type], text_type)
    return nodes





