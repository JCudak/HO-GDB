class Edge:
    def __init__(self, start_node, end_node, relationship_type):
        self.start_node = start_node
        self.end_node = end_node
        self.relationship_type = relationship_type

    def __repr__(self):
        return f"({self.start_node}) --[{self.relationship_type}]--> ({self.end_node})"

    def __eq__(self, other):
        return (self.start_node == other.start_node and
                self.end_node == other.end_node and
                self.relationship_type == other.relationship_type)

    def __hash__(self):
        return hash(self.start_node + self.end_node + self.relationship_type)
