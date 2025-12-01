from quopri import quote

from idna import ulabel

from block import *

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


"""
    ###### space heading
``` ``` code
> (every line) quote
- space(every line) ul
Number dot whitespace, start at 1, increment
"""