def parse_number(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Please enter a correct number!")


def parse_edge_name_input():
    edge_id_str = input("Enter edge id in format (node1, node2): ")
    try:
        node1, node2 = map(int, edge_id_str.strip("() ").split(","))
        return node1, node2
    except ValueError:
        print("Invalid input format. Please use the format (node1, node2, key).")
        return None
