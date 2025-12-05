# ast_nodes.py
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, List, Optional, Deque
from collections import deque


@dataclass
class ASTNode:
    """
    Generic AST node.

    kind:  node type (e.g., "Program", "IfStatement", "BinOp")
    value: optional value (e.g., identifier name, operator symbol, literal)
    children: list of child ASTNodes
    """
    kind: str
    value: Optional[Any] = None
    children: List["ASTNode"] = field(default_factory=list)

    def add_child(self, child: "ASTNode") -> None:
        if child is not None:
            self.children.append(child)


def make_leaf(kind: str, value: Any) -> ASTNode:
    """Helper for simple leaf nodes."""
    return ASTNode(kind=kind, value=value, children=[])


def level_order_string(root: Optional[ASTNode]) -> str:
    """
    Return a level-order (BFS) traversal string in the required format:
      - Each level on its own line
      - Levels separated by *two* blank lines
      - Nodes within a level separated by " # "
    """
    if root is None:
        return ""

    lines: List[str] = []
    queue: Deque[ASTNode] = deque([root])

    while queue:
        level_size = len(queue)
        level_nodes: List[str] = []

        for _ in range(level_size):
            node = queue.popleft()
            if node.value is not None:
                label = f"{node.kind}({node.value})"
            else:
                label = node.kind

            level_nodes.append(label)
            for child in node.children:
                queue.append(child)

        lines.append(" # ".join(level_nodes))

    # Two blank lines between levels
    return "\n\n".join(lines)