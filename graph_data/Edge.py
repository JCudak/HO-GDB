from graph_data.Node import Node


class Edge:
    def __init__(self, start_node_name: str, end_node_name: str, relationship_type: str):
        self.start_node: Node = Node(start_node_name)
        self.end_node: Node = Node(end_node_name)
        self.relationship_type: str = relationship_type

    def __repr__(self):
        return f"({self.start_node},{self.end_node})->[{self.relationship_type}]"

    def __eq__(self, other):
        return (self.start_node == other.start_node and
                self.end_node == other.end_node and
                self.relationship_type == other.relationship_type)

    def __hash__(self):
        return hash((self.start_node, self.end_node, self.relationship_type))
