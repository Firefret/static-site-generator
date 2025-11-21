class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children or []
        self.props = props or {}

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if self.props:
            serialized_props = " "
            for key, value in self.props.items():
                if value is None or value == "": ## Boolean props
                    serialized_props += f'{key} '
                else:
                    serialized_props += f'{key}="{value}" '
            return serialized_props.rstrip()
        return ""

    def __repr__(self):
        return f"Tag: {self.tag}, Value: {self.value}, Children: {self.children}, Props: {self.props}"
