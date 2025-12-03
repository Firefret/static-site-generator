from block import *
from parsing_inline import *
from htmlnode import *

def markdown_to_blocks(markdown:str):
    blocks = markdown.split("\n\n")
    for block in blocks:
        if len(block) == 0:
            blocks.remove(block)
        block = block.strip()

    return blocks

def block_to_block_type(block:str):
    if (block.startswith("# ") or
        block.startswith("## ") or
        block.startswith("### ") or
        block.startswith("#### ") or
        block.startswith("##### ") or
        block.startswith("###### ")
    ):
        return BlockType.HEADING
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    lines = block.split("\n")
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST
    if all(line.startswith(f"{i}. ") for i, line in enumerate(lines, start=1)):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def markdown_to_leaves(markdown:str):
    text_nodes = text_to_textnodes(markdown)
    leaves = []
    for text_node in text_nodes:
        leaves.append(text_node_to_html_node(text_node))
    return leaves

def quote_block_to_html_node(block:str):
    lines = block.split("\n")
    lines = [line.lstrip(">") for line in lines]
    block = "<br>".join(lines).strip()
    leaves = markdown_to_leaves(block)
    quote_node = ParentNode("blockquote", leaves)
    return quote_node

def unordered_list_block_to_html_node(block:str):
    lines = block.split("\n")
    list_items = []
    for line in lines:
        list_item = line.lstrip("- ")
        item_node = ParentNode("li", markdown_to_leaves(list_item))
        list_items.append(item_node)
    list_node = ParentNode("ul", list_items)
    return list_node

def ordered_list_block_to_html_node(block:str):
    lines = block.split("\n")
    list_items = []
    for index, line in enumerate(lines, start=1):
        list_item = line.lstrip(f"{index}. ")
        item_node = ParentNode("li", markdown_to_leaves(list_item))
        list_items.append(item_node)
    list_node = ParentNode("ol", list_items)
    return list_node

def code_block_to_html_node(block:str):
    block = block.strip("```")
    code_node = LeafNode("code", block)
    return ParentNode("pre", [code_node])

def heading_block_to_html_node(block:str):
    heading_level = len(block) - len(block.lstrip("#"))
    text = block.lstrip("# ")
    lines = text.split("\n")
    text = "<br>".join(lines).strip()
    leaves = markdown_to_leaves(text)
    heading_node = ParentNode(f"h{heading_level}", leaves)
    return heading_node

def paragraph_block_to_html_node(block:str):
    lines = block.split("\n")
    block = "<br>".join(lines).strip()
    leaves = markdown_to_leaves(block)
    paragraph_node = ParentNode("p", leaves)
    return paragraph_node


def markdown_to_html_node(markdown:str):
    blocks = markdown_to_blocks(markdown)
    block_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.HEADING:
            block_nodes.append(heading_block_to_html_node(block))
        elif block_type == BlockType.QUOTE:
            block_nodes.append(quote_block_to_html_node(block))
        elif block_type == BlockType.UNORDERED_LIST:
            block_nodes.append(unordered_list_block_to_html_node(block))
        elif block_type == BlockType.ORDERED_LIST:
            block_nodes.append(ordered_list_block_to_html_node(block))
        elif block_type == BlockType.CODE:
            block_nodes.append(code_block_to_html_node(block))
        elif block_type == BlockType.PARAGRAPH:
            block_nodes.append(paragraph_block_to_html_node(block))
        else:
            raise TypeError("Invalid block type")
    return ParentNode("div", block_nodes)