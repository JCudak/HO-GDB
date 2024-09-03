from graph_data.Node import Node
from graph_data.Edge import Edge
from graph_data.HyperEdge import HyperEdge
import pandas as pd
import ast


class GraphStorage:
    def __init__(self, db):
        """Initialize GraphStorage with a database connection."""
        self.nodes = set()
        self.edges = set()
        self.hyper_edges = set()
        self.db = db

    def _with_session(self, operation):
        """Context manager for database session handling."""
        with self.db._driver.session() as session:
            operation(session)

    def add_node(self, node_name: str):
        """Create a Node instance and add it to both the graph and the database."""
        self._add_node_to_database(node_name)
        node = Node(node_name)
        self.nodes.add(node)

    def _add_node_to_database(self, node_name: str):
        """Add a node to the database."""

        def operation(session):
            self.db.add_node(session, labels=["Node"], properties={"name": node_name})

        self._with_session(operation)

    def delete_node(self, node_name: str):
        """Delete a Node by its name from the graph and the database."""
        node = Node(node_name)

        if node in self.nodes:
            self.nodes.remove(node)

        self._delete_node_from_database(node_name)

    def _delete_node_from_database(self, node_name: str):
        """Remove a node from the database."""

        def operation(session):
            self.db.delete_node(session, labels=["Node"], properties={"name": node_name})

        self._with_session(operation)

    def add_edge(self, start_node_name: str, end_node_name: str, relationship_type: str = "CONNECTED"):
        """Create an Edge instance and add it to both the graph and the database."""
        edge = Edge(start_node_name, end_node_name, relationship_type)
        self.edges.add(edge)
        self._add_edge_to_database(start_node_name, end_node_name, relationship_type)

    def _add_edge_to_database(self, start_node_name: str, end_node_name: str, relationship_type: str):
        """Add an edge to the database."""

        def operation(session):
            self.db.add_edge(
                session,
                start_node_labels=["Node"],
                start_node_properties={"name": start_node_name},
                end_node_labels=["Node"],
                end_node_properties={"name": end_node_name},
                relationship_type=relationship_type
            )

        self._with_session(operation)

    def delete_edge(self, start_node_name: str, end_node_name: str, relationship_type: str = "CONNECTED"):
        """Remove an Edge instance from the graph and the database."""
        edge = Edge(start_node_name, end_node_name, relationship_type)
        if edge in self.edges:
            self.edges.remove(edge)

        self._delete_edge_from_database(start_node_name, end_node_name, relationship_type)

    def _delete_edge_from_database(self, start_node_name: str, end_node_name: str, relationship_type: str):
        """Remove an edge from the database."""

        def operation(session):
            self.db.delete_edge(
                session,
                start_node_labels=["Node"],
                start_node_properties={"name": start_node_name},
                end_node_labels=["Node"],
                end_node_properties={"name": end_node_name},
                relationship_type=relationship_type
            )

        self._with_session(operation)

    def add_hyper_edge(self, node_names: frozenset, relationship_type: str = "CONNECTED"):
        """Create an Edge instance and add it to both the graph and the database."""
        hyper_edge = HyperEdge(node_names, relationship_type)
        self.hyper_edges.add(hyper_edge)

    def delete_hyper_edge(self, node_names: frozenset, relationship_type: str = "CONNECTED"):
        """Remove a HyperEdge instance from the graph."""
        hyper_edge = HyperEdge(node_names, relationship_type)
        self.hyper_edges.discard(hyper_edge)

    def import_nodes_from_csv(self, file_path: str, clear: bool = True):
        """Import nodes from a CSV file."""
        if clear:
            self.nodes.clear()

        df = pd.read_csv(file_path)

        for _, row in df.iterrows():
            properties = ast.literal_eval(row['properties'])
            self.add_node(properties['name'])

        def operation(session):
            self.db.import_nodes_from_csv(session, file_path)

        self._with_session(operation)

    def import_edges_from_csv(self, file_path: str, clear: bool = True):
        """Import edges from a CSV file."""
        if clear:
            self.edges.clear()

        df = pd.read_csv(file_path)

        for _, row in df.iterrows():
            start_node_name: str = row['start_name']
            end_node_name: str = row['end_name']
            relationship_type: str = row['type']
            self.add_edge(start_node_name, end_node_name, relationship_type)

        def operation(session):
            self.db.import_edges_from_csv(session, file_path)

        self._with_session(operation)

    def clear_graph(self):
        """Clear the graph storage."""
        self.nodes.clear()
        self.edges.clear()
        self.hyper_edges.clear()

        def operation(session):
            self.db.clear_data(session)

        self._with_session(operation)

    def __str__(self):
        """Return a string representation of the graph storage."""
        return (
            f"Nodes: {self.nodes}\n"
            f"Edges: {self.edges}\n"
            f"HyperEdges: {self.hyper_edges}"
        )
