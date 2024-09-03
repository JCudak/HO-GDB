class Edge:
    def __init__(self, start_node: str, end_node: str, relationship_type: str):
        self.start_node: str = start_node
        self.end_node: str = end_node
        self.relationship_type: str = relationship_type

    def __repr__(self):
        return f"({self.start_node}) --[{self.relationship_type}]--> ({self.end_node})"

    def __eq__(self, other):
        return (self.start_node == other.start_node and
                self.end_node == other.end_node and
                self.relationship_type == other.relationship_type)

    def __hash__(self):
        return hash((self.start_node, self.end_node, self.relationship_type))
