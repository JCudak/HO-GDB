import os

from database import Database
from database.KuzuDatabase import KuzuDatabase
from database.Neo4jDatabase import Neo4jDatabase
from utils import parse_number, parse_and_validate_edges, parse_and_validate_hyper_edges, parse_and_validate_nodes
from graph_data.GraphStorage import GraphStorage
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()


def modify_graph_gui():
    """Graph modification GUI."""

    def add_nodes():
        node_names = input("Enter node name(s) separated by semi-colon: ")
        valid_node_names = parse_and_validate_nodes(node_names)
        for node_name in valid_node_names:
            graph_storage.add_node(node_name)
        print("Node(s) added successfully.")

    def delete_nodes():
        node_names = input("Enter node name(s) to delete separated by semi-colon: ")
        valid_node_names = parse_and_validate_nodes(node_names)
        for node_name in valid_node_names:
            graph_storage.delete_node(node_name)
        print("Node(s) deleted successfully.")

    def add_edges():
        edges_input = input("Enter edge(s) in format (relationship_name,start_node,end_node) separated by semi-colon: ")
        edges = parse_and_validate_edges(edges_input)
        for relationship_name, start_node_name, end_node_name in edges:
            graph_storage.add_edge(start_node_name.strip(), end_node_name.strip(), relationship_name.strip())
        print("Edges added successfully.")

    def delete_edges():
        edges_input = input(
            "Enter edge(s) to delete in format (relationship_name,start_node,end_node) separated by semi-colon: ")
        edges = parse_and_validate_edges(edges_input)
        for relationship_name, start_node_name, end_node_name in edges:
            graph_storage.delete_edge(start_node_name.strip(), end_node_name.strip(), relationship_name.strip())
        print("Edges deleted successfully.")

    def add_hyper_edges():
        hyper_edges_input = input("Enter hyper edge(s) in format (node_1,node_2,...,node_n) separated by semi-colon: ")
        hyper_edges = parse_and_validate_hyper_edges(hyper_edges_input)
        for hyper_edge in hyper_edges:
            graph_storage.add_hyper_edge(hyper_edge)
        print("Hyper edges added successfully.")

    def delete_hyper_edges():
        hyper_edges_input = input(
            "Enter hyper edge(s) to delete in format (node_1,node_2,...,node_n) separated by semi-colon: ")
        hyper_edges = parse_and_validate_hyper_edges(hyper_edges_input)
        for hyper_edge in hyper_edges:
            graph_storage.delete_hyper_edge(hyper_edge)
        print("Hyper edges deleted successfully.")

    options = {
        1: add_nodes,
        2: delete_nodes,
        3: add_edges,
        4: delete_edges,
        5: add_hyper_edges,
        6: delete_hyper_edges,
    }

    while True:
        print("\nChoose an option:\n"
              "1 - Add Node(s)\n"
              "2 - Delete Node(s)\n"
              "3 - Add Edge(s)\n"
              "4 - Delete Edge(s)\n"
              "5 - Add Hyper Edge(s)\n"
              "6 - Delete Hyper Edge(s)\n"
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
        graph_storage.clear_graph()
        print("Graph cleared successfully.")

    def import_graph():
        graph_storage.import_graph()
        print("Graph imported successfully.")

    def export_graph():
        graph_storage.export_graph()
        print("Graph exported successfully.")

    def display_higher_order_graph():
        print(graph_storage)

    options = {
        1: import_graph,
        2: lambda: modify_graph_gui(),
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
    db: Database
    if os.getenv("DATABASE_PROVIDER") == "NEO4J":
        db = Neo4jDatabase()
    elif os.getenv("DATABASE_PROVIDER") == "KUZU":
        db = KuzuDatabase()
    graph_storage = GraphStorage(db)
    try:
        gui()
    finally:
        db.end_session()
