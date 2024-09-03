from graph_data.Node import Node


class HyperEdge:
    def __init__(self, nodes: frozenset[Node], relationship_type: str):
        self.nodes: frozenset[Node] = nodes
        self.relationship_type: str = relationship_type

    def __repr__(self):
        return f"""({', '.join(f"'{item}'" for item in self.nodes)})->[{self.relationship_type}]"""

    def __eq__(self, other):
        return (self.nodes == other.nodes and
                self.relationship_type == other.relationship_type)

    def __hash__(self):
        return hash((self.nodes, self.relationship_type))
