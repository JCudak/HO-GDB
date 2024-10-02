from database.Database import *
import kuzu


class KuzuDatabase(Database):
    def __init__(self):

        self.db = kuzu.Database("./demo_db")
        self.session = kuzu.Connection(self.db)

    def _execute_query(self, session, query: str, parameters: Optional[Dict] = None) -> List[Dict]:
        """Execute a Cypher query and return the results."""
        session.execute(query)

    def add_node(self, session, labels: Optional[List[str]] = None, properties: Optional[Dict[str, str]] = None):
        """Add a node to the database."""
        query = f"""CREATE NODE TABLE IF NOT EXISTS {properties["name"]}(name STRING, PRIMARY KEY (name))"""
        self._execute_query(session, query)

    def delete_node(self, session, labels: List[str], properties: Dict[str, str]):
        """Delete a node"""
        query = f"""
        DROP TABLE {properties["name"]}
        """
        self._execute_query(session, query)

    def add_edge(self, session, start_node_labels: List[str], start_node_properties: Dict[str, str],
                 end_node_labels: List[str], end_node_properties: Dict[str, str], relationship_name: str):
        """Add a relationship (edge) between two nodes."""
        query = f"""
        CREATE REL TABLE IF NOT EXISTS {relationship_name}(FROM {start_node_properties["name"]} TO {end_node_properties["name"]})
        """
        self._execute_query(session, query)

    def delete_edge(self, session, start_node_labels: List[str], start_node_properties: Dict[str, str],
                    end_node_labels: List[str], end_node_properties: Dict[str, str], relationship_name: str):
        """Delete a relationship (edge) between two nodes."""
        query = f"""
                DROP TABLE {relationship_name}
        """
        self._execute_query(session, query)

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
