import os
from typing import Union

from pydantic import BaseModel

NodeType = Union[str, "Node"]
NodeListType = list[NodeType]


class Node(BaseModel):
    slug: str
    children: NodeListType = []

    @classmethod
    def parse_node(cls, node):
        if isinstance(node, str):
            return node
        elif isinstance(node, dict):
            for key, value in node.items():
                return cls(
                    slug=key, children=[cls.parse_node(child) for child in value]
                )
        else:
            raise ValueError(f"Invalid node type: {type(node)}")


class BookMDModel(BaseModel):
    nodes: NodeListType

    @classmethod
    def parse_nodes(cls, nodes):
        return [Node.parse_node(node) for node in nodes]

    @classmethod
    def from_front_matter(cls, data: dict):
        data["nodes"] = cls.parse_nodes(data.get("nodes", []))
        return cls(**data)

    def gather_markdown_files(
        self, base_path
    ) -> list[tuple[str, Union[str, None], int]]:
        markdown_files = []

        def _gather_files(node, parent, current_path, order):
            if isinstance(node, str):
                markdown_files.append(
                    (os.path.join(current_path, f"{node}.md"), parent, order)
                )
            elif isinstance(node, Node):
                for idx, child in enumerate(node.children, start=1):
                    _gather_files(child, node.name, current_path, idx)

        for idx, node in enumerate(self.nodes, start=1):
            _gather_files(node, None, base_path, idx)

        return markdown_files


class BookMDNodeModel(BaseModel):
    heading: str | None = None
    title: str
    subheading: str | None = None
