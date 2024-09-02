from graph_data.Node import Node
from graph_data.Edge import Edge
from graph_data.HyperEdge import HyperEdge


class GraphStorage:
    def __init__(self, db):
        self.nodes = set()
        self.edges = set()
        self.hyper_edges = set()
        self.db = db

    def add_node(self, node_name: str):
        """Create a Node instance from a name and add it to the graph."""
        self.add_node_to_database(node_name)
        self.nodes.add(Node(node_name))

    def add_node_to_database(self, node_name: str):
        with self.db._driver.session() as session:
            self.db.add_node(session, labels=["Node"], properties={"name": node_name})

    def delete_node_from_database(self, node_name: str):
        with self.db._driver.session() as session:
            self.db.delete_node(session, labels=["Node"], properties={"name": node_name})

    def add_edge_to_database(self, start_node_name: str, end_node_name: str, relationship_type: str):
        with self.db._driver.session() as session:
            self.db.add_edge(session,
                             start_node_labels=["Node"],
                             start_node_properties={"name": start_node_name},
                             end_node_labels=["Node"],
                             end_node_properties={"name": end_node_name},
                             relationship_type=relationship_type)

    def delete_edge_from_database(self, start_node_name: str, end_node_name: str, relationship_type: str):
        with self.db._driver.session() as session:
            self.db.delete_edge(session,
                                start_node_labels=["Node"],
                                start_node_properties={"name": start_node_name},
                                end_node_labels=["Node"],
                                end_node_properties={"name": end_node_name},
                                relationship_type="CONNECTED")

    def delete_node(self, node_name: str):
        """Delete a Node by its name."""
        node = Node(node_name)

        if node in self.nodes:
            self.nodes.remove(node)

        self.delete_node_from_database(node_name)

    def add_edge(self, start_node_name: str, end_node_name: str, relationship_type: str = "CONNECTED"):
        """Add an Edge instance to the graph."""
        edge = Edge(start_node_name, end_node_name, relationship_type)
        self.edges.add(edge)
        self.add_edge_to_database(start_node_name, end_node_name, relationship_type)

    def delete_edge(self, start_node_name: str, end_node_name: str, relationship_type: str = "CONNECTED"):
        """Remove an Edge instance from the graph."""
        edge = Edge(start_node_name, end_node_name, relationship_type)
        if edge in self.edges:
            self.edges.remove(edge)

        self.delete_edge_from_database(start_node_name, end_node_name, relationship_type)

    def add_hyper_edge(self, hyper_edge: HyperEdge):
        """Add a HyperEdge instance to the graph."""
        self.hyper_edges.add(hyper_edge)

    def delete_hyper_edge(self, hyper_edge: HyperEdge):
        """Remove a HyperEdge instance from the graph."""
        if hyper_edge in self.hyper_edges:
            self.hyper_edges.remove(hyper_edge)

    def __str__(self):
        return f"Nodes: {self.nodes}\nEdges: {self.edges}\nHyperEdges: {self.hyper_edges}"
