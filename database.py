import ast
import os
from typing import List, Dict, Optional
from dotenv import load_dotenv
import pandas as pd
from neo4j import GraphDatabase

# Load environment variables from the .env file
load_dotenv()

class Database:
    def __init__(self):
        self._db_uri = os.getenv("DB_URI")
        self._db_username = os.getenv("DB_USERNAME")
        self._db_password = os.getenv("DB_PASSWORD")
        self._driver = GraphDatabase.driver(self._db_uri, auth=(self._db_username, self._db_password))

    def _execute_query(self, session, query: str, parameters: Optional[Dict] = None) -> List[Dict]:
        """Execute a Cypher query and return the results."""
        result = session.run(query, parameters or {})
        return [record for record in result]

    def format_properties(self, properties: Optional[Dict[str, str]]) -> str:
        """Convert a dictionary of properties to a Cypher-compatible string."""
        if not properties:
            return ""
        return "{" + ", ".join(f"{k}: '{v}'" for k, v in properties.items()) + "}"

    def format_labels(self, labels: Optional[List[str]]) -> str:
        """Convert a list of labels to a Cypher-compatible string."""
        if not labels:
            return ""
        return ":" + ":".join(labels)

    def export_nodes_to_csv(self, session, file_name: str):
        """Export nodes to a CSV file."""
        query = """
        MATCH (n)
        RETURN labels(n) AS labels, properties(n) AS properties
        """
        records = self._execute_query(session, query)
        df = pd.DataFrame(records)
        df.to_csv(file_name, index=False)

    def export_edges_to_csv(self, session, file_name: str):
        """Export edges to a CSV file."""
        query = """
        MATCH (a)-[r]->(b)
        RETURN a.name AS start_name, b.name AS end_name, type(r) AS type, properties(r) AS properties
        """
        records = self._execute_query(session, query)
        df = pd.DataFrame(records)
        df.to_csv(file_name, index=False)

    def import_nodes_from_csv(self, session, file_name: str):
        """Import nodes from a CSV file into Neo4j."""
        df = pd.read_csv(file_name)
        for _, row in df.iterrows():
            labels = row['labels'].strip("[]").replace("'", "").split(", ")
            properties = ast.literal_eval(row['properties'])
            labels_str = self.format_labels(labels)
            properties_str = self.format_properties(properties)
            query = f"""
            MERGE (n{labels_str} {properties_str})
            """
            self._execute_query(session, query)

    def import_edges_from_csv(self, session, file_name: str):
        """Import edges from a CSV file into Neo4j."""
        df = pd.read_csv(file_name)
        for _, row in df.iterrows():
            start_name = row['start_name']
            end_name = row['end_name']
            relationship_type = row['type']
            properties = row['properties'] if not pd.isna(row['properties']) else '{}'
            properties_dict = ast.literal_eval(properties)
            properties_str = self.format_properties(properties_dict)
            query = f"""
            MATCH (a {{name: '{start_name}'}}), (b {{name: '{end_name}'}})
            MERGE (a)-[r:{relationship_type} {properties_str}]->(b)
            """
            self._execute_query(session, query)

    def add_node(self, session, labels: Optional[List[str]] = None, properties: Optional[Dict[str, str]] = None):
        """Add a node to the database."""
        labels_str = self.format_labels(labels)
        properties_str = self.format_properties(properties)
        query = f"""
        MERGE (n{labels_str} {properties_str})
        """
        self._execute_query(session, query)

    def delete_node(self, session, labels: List[str], properties: Dict[str, str]):
        """Delete a node and all its connected edges."""
        labels_str = self.format_labels(labels)
        properties_str = self.format_properties(properties)
        query = f"""
        MATCH (n{labels_str} {properties_str})
        DETACH DELETE n
        """
        self._execute_query(session, query)

    def add_edge(self, session, start_node_labels: List[str], start_node_properties: Dict[str, str],
                 end_node_labels: List[str], end_node_properties: Dict[str, str], relationship_type: str):
        """Add a relationship (edge) between two nodes."""
        start_labels_str = self.format_labels(start_node_labels)
        end_labels_str = self.format_labels(end_node_labels)
        start_properties_str = self.format_properties(start_node_properties)
        end_properties_str = self.format_properties(end_node_properties)
        query = f"""
        MERGE (start{start_labels_str} {start_properties_str})
        MERGE (end{end_labels_str} {end_properties_str})
        MERGE (start)-[r:{relationship_type}]->(end)
        RETURN start.id AS startId, end.id AS endId
        """
        self._execute_query(session, query)

    def delete_edge(self, session, start_node_labels: List[str], start_node_properties: Dict[str, str],
                    end_node_labels: List[str], end_node_properties: Dict[str, str], relationship_type: str):
        """Delete a relationship (edge) between two nodes."""
        start_labels_str = self.format_labels(start_node_labels)
        end_labels_str = self.format_labels(end_node_labels)
        start_properties_str = self.format_properties(start_node_properties)
        end_properties_str = self.format_properties(end_node_properties)
        query = f"""
        MATCH (start{start_labels_str} {start_properties_str})
        MATCH (end{end_labels_str} {end_properties_str})
        OPTIONAL MATCH (start)-[r:{relationship_type}]->(end)
        DELETE r
        """
        self._execute_query(session, query)

    def clear_data(self, session):
        """Remove all data from the database."""
        query = """
        MATCH (n)
        DETACH DELETE n
        """
        self._execute_query(session, query)

    def end_session(self):
        """Close the database connection."""
        self._driver.close()
