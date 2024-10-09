from database.Database import *
import kuzu


class KuzuDatabase(Database):
    def __init__(self):
        self.db = kuzu.Database("./demo_db")
        self.session = kuzu.Connection(self.db)

        self._create_schema()

    def _create_schema(self):
        query = f"""CREATE NODE TABLE IF NOT EXISTS GNode(name STRING, PRIMARY KEY (name))"""
        self._execute_query(self.session, query)

        query = f"""CREATE REL TABLE IF NOT EXISTS Connects(FROM GNode TO GNode)"""
        self._execute_query(self.session, query)

    def _execute_query(self, session, query: str, parameters: Optional[Dict] = None) -> List[Dict]:
        """Execute a Cypher query and return the results."""
        session.execute(query)

    def _replace_slash(self, s: str) -> str:
        """
        Replace all occurrences of '/' with '//' in the given string.
        """
        return s.replace('\\', '/')

    def export_nodes_to_csv(self, session, file_name: str):
        """Export nodes to a CSV file."""
        query = f"""
        COPY (MATCH (u:GNode) RETURN u.name AS name) TO '{self._replace_slash(file_name)}' (HEADER=true, DELIM="|");
        """
        self._execute_query(session, query)

    def export_edges_to_csv(self, session, file_name: str):
        """Export edges to a CSV file."""
        query = f"""
        COPY (MATCH (a:GNode)-[f:Connects]->(b:GNode) RETURN a.name AS start_name, b.name AS end_name) 
        TO '{self._replace_slash(file_name)}' (HEADER=true, DELIM="|");
        """
        self._execute_query(session, query)

    def import_nodes_from_csv(self, session, file_name: str):
        """Import nodes from a CSV file into Neo4j."""

        query = f"""
        COPY GNode FROM '{self._replace_slash(file_name)}' (HEADER=true, DELIM="|");
        """
        self._execute_query(session, query)

    def import_edges_from_csv(self, session, file_name: str):
        """Import edges from a CSV file into Neo4j."""

        query = f"""
        COPY Connects FROM '{self._replace_slash(file_name)}' (HEADER=true, DELIM="|");
        """
        self._execute_query(session, query)

    def add_node(self, session, labels: Optional[List[str]] = None, properties: Optional[Dict[str, str]] = None):
        """Add a node to the database."""

        label_str = self.format_labels(labels)
        properties_str = self.format_properties(properties)

        query = f"""
                CREATE (n{label_str} {properties_str})
                RETURN n
                """
        self._execute_query(self.session, query)

    def delete_node(self, session, labels: List[str], properties: Dict[str, str]):
        """Delete a node"""

        label_str = self.format_labels(labels)
        properties_str = self.format_properties(properties)
        query = f""" MATCH(n{label_str} {properties_str}) DELETE n"""
        self._execute_query(self.session, query)

    def add_edge(self, session, start_node_labels: List[str], start_node_properties: Dict[str, str],
                 end_node_labels: List[str], end_node_properties: Dict[str, str], relationship_name: str = 'Connects'):
        """Add a relationship (edge) between two nodes."""

        start_label_str = self.format_labels(start_node_labels)
        end_label_str = self.format_labels(end_node_labels)

        start_properties_str = self.format_properties(start_node_properties)
        end_properties_str = self.format_properties(end_node_properties)

        query = f""" MATCH(a{start_label_str} {start_properties_str}), (b{end_label_str} {end_properties_str})
        CREATE(a) - [r:{relationship_name}]->(b)"""
        self._execute_query(self.session, query)

    def delete_edge(self, session, start_node_labels: List[str], start_node_properties: Dict[str, str],
                    end_node_labels: List[str], end_node_properties: Dict[str, str], relationship_name: str):
        """Delete a relationship (edge) between two nodes."""

        start_label_str = self.format_labels(start_node_labels)
        end_label_str = self.format_labels(end_node_labels)

        start_properties_str = self.format_properties(start_node_properties)
        end_properties_str = self.format_properties(end_node_properties)

        query = f""" MATCH(a{start_label_str} {start_properties_str})-[r:Connects]->(b{end_label_str} {end_properties_str}) 
        DELETE r"""
        self._execute_query(self.session, query)

    def clear_data(self, session):
        """Remove all data from the database."""
        query = """
        MATCH (n)
        DETACH DELETE n
        """
        self._execute_query(session, query)

    def start_session(self):
        """Open a new database connection."""
        return self.session

    def end_session(self):
        """Close the database connection."""
        pass
