def markdown_to_blocks(markdown:str):
    blocks = markdown.split("\n\n")
    for block in blocks:
        if len(block) == 0:
            blocks.remove(block)
        block = block.strip()

    return blocks
