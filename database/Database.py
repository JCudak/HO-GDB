import ast
import os
from abc import abstractmethod
from typing import List, Dict, Optional
from dotenv import load_dotenv
import pandas as pd


class Database:
    @abstractmethod
    def export_nodes_to_csv(self, session, file_name: str):
        """Export nodes to a CSV file."""
        pass

    @abstractmethod
    def export_edges_to_csv(self, session, file_name: str):
        """Export edges to a CSV file."""
        pass

    @abstractmethod
    def import_nodes_from_csv(self, session, file_name: str):
        """Import nodes from a CSV file into Neo4j."""
        pass

    @abstractmethod
    def import_edges_from_csv(self, session, file_name: str):
        """Import edges from a CSV file into Neo4j."""
        pass

    @abstractmethod
    def add_node(self, session, labels: Optional[List[str]] = None, properties: Optional[Dict[str, str]] = None):
        """Add a node to the database."""
        pass

    @abstractmethod
    def delete_node(self, session, labels: List[str], properties: Dict[str, str]):
        """Delete a node and all its connected edges."""
        pass

    @abstractmethod
    def add_edge(self, session, start_node_labels: List[str], start_node_properties: Dict[str, str],
                 end_node_labels: List[str], end_node_properties: Dict[str, str], relationship_name: str):
        """Add a relationship (edge) between two nodes."""
        pass

    @abstractmethod
    def delete_edge(self, session, start_node_labels: List[str], start_node_properties: Dict[str, str],
                    end_node_labels: List[str], end_node_properties: Dict[str, str], relationship_name: str):
        """Delete a relationship (edge) between two nodes."""
        pass

    @abstractmethod
    def clear_data(self, session):
        """Remove all data from the database."""
        pass

    @abstractmethod
    def end_session(self):
        """Close the database connection."""
        pass
