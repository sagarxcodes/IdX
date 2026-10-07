from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class KnowledgeNode:

    node_id: str
    node_type: str
    attributes: Dict = field(
        default_factory=dict
    )


@dataclass
class KnowledgeEdge:

    source: str
    target: str
    relation: str
    weight: float = 1.0


class KnowledgeGraph:

    def __init__(self):

        self.nodes: Dict[str, KnowledgeNode] = {}
        self.edges: List[KnowledgeEdge] = []

    def add_node(
        self,
        node_id: str,
        node_type: str,
        attributes=None,
    ):

        self.nodes[node_id] = KnowledgeNode(
            node_id=node_id,
            node_type=node_type,
            attributes=attributes or {},
        )

    def connect(
        self,
        source: str,
        target: str,
        relation: str,
        weight: float = 1.0,
    ):

        self.edges.append(
            KnowledgeEdge(
                source=source,
                target=target,
                relation=relation,
                weight=weight,
            )
        )

    def neighbors(self, node_id: str):

        result = []

        for edge in self.edges:

            if edge.source == node_id:
                result.append(
                    (edge.target, edge.relation)
                )

            elif edge.target == node_id:
                result.append(
                    (edge.source, edge.relation)
                )

        return result
