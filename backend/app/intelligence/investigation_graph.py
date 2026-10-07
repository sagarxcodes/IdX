from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class InvestigationNode:
    id: str
    name: str
    description: str = ""
    importance: float = 1.0


@dataclass
class InvestigationEdge:
    source: str
    target: str
    relation: str
    weight: float = 1.0


@dataclass
class InvestigationGraph:
    """
    Generic investigation graph.

    Nodes represent things that may matter to a decision.
    Edges represent relationships between them.

    The graph is deliberately domain-independent.
    """

    nodes: Dict[str, InvestigationNode] = field(default_factory=dict)
    edges: List[InvestigationEdge] = field(default_factory=list)

    def add_node(
        self,
        node_id: str,
        name: str,
        description: str = "",
        importance: float = 1.0,
    ) -> None:
        self.nodes[node_id] = InvestigationNode(
            id=node_id,
            name=name,
            description=description,
            importance=importance,
        )

    def connect(
        self,
        source: str,
        target: str,
        relation: str,
        weight: float = 1.0,
    ) -> None:
        self.edges.append(
            InvestigationEdge(
                source=source,
                target=target,
                relation=relation,
                weight=weight,
            )
        )

    def missing_nodes(self, known: List[str]) -> List[InvestigationNode]:
        return [
            node
            for node_id, node in self.nodes.items()
            if node_id not in known
        ]
