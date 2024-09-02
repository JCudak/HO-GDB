import os

from database import Database
from utils import parse_number  # Assuming parse_number is defined in utils


def gui2(db: Database):
    def add_nodes():
        node_names = input("Enter the name of the Node(s): ")
        with db._driver.session() as session:
            for node_name in node_names.split(" "):
                db.add_node(session, labels=["Node"], properties={"name": node_name})
        print("Node(s) added successfully.")

    def delete_nodes():
        node_names = input("Enter Node name(s) to delete: ")
        with db._driver.session() as session:
            for node_name in node_names.split(" "):
                db.delete_node(session, labels=["Node"], properties={"name": node_name})
        print("Node(s) deleted successfully.")

    def add_edges():
        edges_input = input("Enter Edge(s) in format (start_node,end_node): ")
        edges = [tuple(edge.strip('() ').split(',')) for edge in edges_input.split(' ')]

        with db._driver.session() as session:
            for start_node_name, end_node_name in edges:
                start_node_name = start_node_name.strip()
                end_node_name = end_node_name.strip()

                db.add_edge(session,
                            start_node_labels=["Node"],
                            start_node_properties={"name": start_node_name},
                            end_node_labels=["Node"],
                            end_node_properties={"name": end_node_name},
                            relationship_type="CONNECTED")
        print("Edges added successfully.")

    def delete_edges():
        edges_input = input("Enter Edge(s) to delete in  format (start_node,end_node): ")
        edges = [tuple(edge.strip('() ').split(',')) for edge in edges_input.split(' ')]

        with db._driver.session() as session:
            for start_node_name, end_node_name in edges:
                start_node_name = start_node_name.strip()
                end_node_name = end_node_name.strip()

                db.delete_edge(session,
                               start_node_labels=["Node"],
                               start_node_properties={"name": start_node_name},
                               end_node_labels=["Node"],
                               end_node_properties={"name": end_node_name},
                               relationship_type="CONNECTED")
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
        print("Choose an option:\n"
              "1 - Add Node(s)\n"
              "2 - Delete Node(s)\n"
              "3 - Add Edge(s)\n"
              "4 - Delete Edge(s)\n"
              "5 - Add Hyper Edge\n"
              "6 - Delete Hyper Edge\n"
              "7 - Exit")
        choice = parse_number("Enter a number: ")
        if choice == 7:
            break
        option_function = options.get(choice)
        if option_function:
            option_function()


def gui():
    def clear_graph():
        with db._driver.session() as session:
            db.clear_data(session)

    def export_graph():
        export_dir = "exported"
        with db._driver.session() as session:
            db.export_nodes_to_csv(session, os.path.join(export_dir, 'nodes.csv'))
            db.export_edges_to_csv(session, os.path.join(export_dir, 'edges.csv'))
        print("Graph exported successfully.")

    def import_graph():
        import_dir = "exported"
        with db._driver.session() as session:
            db.import_nodes_from_csv(session, os.path.join(import_dir, 'nodes.csv'))
            db.import_edges_from_csv(session, os.path.join(import_dir, 'edges.csv'))
        print("Graph imported successfully.")

    options = {
        1: import_graph,
        2: lambda: gui2(db),
        3: export_graph,
        4: clear_graph,
        5: lambda: None,
        6: lambda: None,
    }

    while True:
        print("Choose an option:\n"
              "1 - Import Graph\n"
              "2 - Modify Graph\n"
              "3 - Export Graph\n"
              "4 - Clear Graph\n"
              "5 - Display Higher-Order Graph(Only for Kuzu)\n"
              "6 - Generate Heterogenous Graph\n"
              "7 - Exit")
        choice = parse_number("Enter a number: ")
        if choice == 7:
            break
        option_function = options.get(choice)
        if option_function:
            option_function()


if __name__ == "__main__":
    db = Database()
    gui()
    db.end_session()
