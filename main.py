import os

from database import Database
from utils import parse_number
from graph_data.GraphStorage import GraphStorage


def parse_and_validate_node_names(node_names: str) -> set:
    """Parse a semi-colon-separated string of node names and return a set of valid names."""
    return {name.strip() for name in node_names.split(';') if name.strip()}


def parse_and_validate_edges(edges_input: str) -> list:
    """Parse a semi-colon-separated string of edges in the format (start_node,end_node) and return a list of tuples."""
    return [tuple(edge.strip('() ').split(',')) for edge in edges_input.split(';')]


def modify_graph_gui(db: Database, graphStorage: GraphStorage):
    """Graph modification GUI."""

    def add_nodes():
        node_names = input("Enter node name(s) separated by semi-colon: ")
        valid_node_names = parse_and_validate_node_names(node_names)
        for node_name in valid_node_names:
            graphStorage.add_node(node_name)
        print("Node(s) added successfully.")

    def delete_nodes():
        node_names = input("Enter node name(s) to delete separated by semi-colon: ")
        valid_node_names = parse_and_validate_node_names(node_names)
        for node_name in valid_node_names:
            graphStorage.delete_node(node_name)
        print("Node(s) deleted successfully.")

    def add_edges():
        edges_input = input("Enter edge(s) in format (start_node,end_node) separated by semi-colon: ")
        edges = parse_and_validate_edges(edges_input)
        for start_node_name, end_node_name in edges:
            graphStorage.add_edge(start_node_name.strip(), end_node_name.strip())
        print("Edges added successfully.")

    def delete_edges():
        edges_input = input("Enter edge(s) to delete in format (start_node,end_node) separated by semi-colon: ")
        edges = parse_and_validate_edges(edges_input)
        for start_node_name, end_node_name in edges:
            graphStorage.delete_edge(start_node_name.strip(), end_node_name.strip())
        print("Edges deleted successfully.")

    options = {
        1: add_nodes,
        2: delete_nodes,
        3: add_edges,
        4: delete_edges,
        5: lambda: None,
        6: lambda: None,
    }

    while True:
        print("\nChoose an option:\n"
              "1 - Add Node(s)\n"
              "2 - Delete Node(s)\n"
              "3 - Add Edge(s)\n"
              "4 - Delete Edge(s)\n"
              "5 - Add Hyper Edge\n"
              "6 - Delete Hyper Edge\n"
              "7 - Exit")
        choice = parse_number("Enter a number: ")
        print()
        if choice == 7:
            break
        option_function = options.get(choice)
        if option_function:
            option_function()


def gui():
    """Main GUI for graph management."""

    def clear_graph():
        graphStorage.clear_graph()
        print("Graph cleared successfully.")

    def export_graph():
        export_dir = "exported"
        os.makedirs(export_dir, exist_ok=True)
        with db._driver.session() as session:
            db.export_nodes_to_csv(session, os.path.join(export_dir, 'nodes.csv'))
            db.export_edges_to_csv(session, os.path.join(export_dir, 'edges.csv'))
        print("Graph exported successfully.")

    def import_graph():
        import_dir = "exported"
        graphStorage.import_nodes_from_csv(os.path.join(import_dir, 'nodes.csv'))
        graphStorage.import_edges_from_csv(os.path.join(import_dir, 'edges.csv'))
        print("Graph imported successfully.")

    def display_higher_order_graph():
        print(graphStorage)

    options = {
        1: import_graph,
        2: lambda: modify_graph_gui(db, graphStorage),
        3: export_graph,
        4: clear_graph,
        5: display_higher_order_graph,
        6: lambda: None,
    }

    while True:
        print("\nChoose an option:\n"
              "1 - Import Graph\n"
              "2 - Modify Graph\n"
              "3 - Export Graph\n"
              "4 - Clear Graph\n"
              "5 - Display Higher-Order Graph (Only for Kuzu)\n"
              "6 - Generate Heterogeneous Graph\n"
              "7 - Exit")
        choice = parse_number("Enter a number: ")
        print()
        if choice == 7:
            break
        option_function = options.get(choice)
        if option_function:
            option_function()


if __name__ == "__main__":
    db = Database()
    graphStorage = GraphStorage(db)
    try:
        gui()
    finally:
        db.end_session()
