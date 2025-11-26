from textnode import *

def split_nodes_delimiter(old_nodes:list[TextNode], delimiter:str, text_type:TextType):
    new_nodes = []

    if delimiter not in text_type_delimiters.values() or delimiter == "":
        raise ValueError("Invalid delimiter")

    for node in old_nodes:
        to_be_nodes = []
        if node.text_type not in [TextType.TEXT, TextType.PLAIN]:
            new_nodes.append(node)
            continue
        if delimiter not in node.text or node.text.count(delimiter)%2 != 0:
            raise ValueError("Delimiter not found or lacks a pair")
        to_be_nodes.extend(node.text.split(delimiter))

        for i in range(0, len(to_be_nodes)):
            if len(to_be_nodes[i])<1:
                continue
            if i%2 != 0: ## because of this the cycle has to be indented, otherwise this , I can't think of a more concise way
                new_nodes.append(TextNode(to_be_nodes[i], text_type))
            else:
                new_nodes.append(TextNode(to_be_nodes[i], TextType.TEXT))
    return new_nodes