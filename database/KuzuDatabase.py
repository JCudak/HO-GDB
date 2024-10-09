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
        print(query)
        session.execute(query)

    def add_node(self, session, labels: Optional[List[str]] = None, properties: Optional[Dict[str, str]] = None):
        """Add a node to the database."""
        if not properties:
            raise ValueError("Properties must be provided to create a node.")

        label_str = ":".join(labels) if labels else "GNode"

        prop_placeholders = ", ".join([f"{key}: '{properties[key]}'" for key in properties])

        query = f"""
                CREATE (n:{label_str} {{{prop_placeholders}}})
                RETURN n
                """
        self._execute_query(self.session, query)

    def delete_node(self, session, labels: List[str], properties: Dict[str, str]):
        """Delete a node"""

        label_str = ":".join(labels) if labels else "GNode"

        prop_placeholders = ", ".join([f"{key}: '{properties[key]}'" for key in properties])
        query = f""" MATCH(n:{label_str} {{{prop_placeholders}}}) DELETE n"""
        self._execute_query(self.session, query)

    def add_edge(self, session, start_node_labels: List[str], start_node_properties: Dict[str, str],
                 end_node_labels: List[str], end_node_properties: Dict[str, str], relationship_name: str = 'Connects'):
        """Add a relationship (edge) between two nodes."""

        start_label_str = ":".join(start_node_labels) if start_node_labels else "GNode"
        end_label_str = ":".join(end_node_labels) if end_node_labels else "GNode"

        start_prop_placeholders = ", ".join([f"{key}: '{start_node_properties[key]}'" for key in start_node_properties])
        end_prop_placeholders = ", ".join([f"{key}: '{end_node_properties[key]}'" for key in end_node_properties])

        query = f""" MATCH(a: {start_label_str} {{{start_prop_placeholders}}}), (b:{end_label_str} {{{end_prop_placeholders}}})
        CREATE(a) - [r:{relationship_name}]->(b)"""
        self._execute_query(self.session, query)

    def delete_edge(self, session, start_node_labels: List[str], start_node_properties: Dict[str, str],
                    end_node_labels: List[str], end_node_properties: Dict[str, str], relationship_name: str):
        """Delete a relationship (edge) between two nodes."""

        start_label_str = ":".join(start_node_labels) if start_node_labels else "GNode"
        end_label_str = ":".join(end_node_labels) if end_node_labels else "GNode"

        start_prop_placeholders = ", ".join([f"{key}: '{start_node_properties[key]}'" for key in start_node_properties])
        end_prop_placeholders = ", ".join([f"{key}: '{end_node_properties[key]}'" for key in end_node_properties])

        query = f""" MATCH(a: {start_label_str} {{{start_prop_placeholders}}})-[r:Connects]->(b:{end_label_str} {{{end_prop_placeholders}}}) 
        DELETE r"""
        self._execute_query(self.session, query)

    def clear_data(self, session):
        """Remove all data from the database."""
        query = """
        MATCH (n)
        DETACH DELETE n
        """
        self._execute_query(session, query)
        query = f"""
                DROP TABLE GNode
                """
        self._execute_query(session, query)
        query = f"""
                        DROP TABLE Connects
                """
        self._execute_query(session, query)

    def start_session(self):
        """Open a new database connection."""
        return self.session

    def end_session(self):
        """Close the database connection."""
        pass
