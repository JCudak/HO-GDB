def parse_number(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Please enter a correct number!")


def parse_and_validate_nodes(nodes_input: str) -> set:
    """Parse a semi-colon-separated string of node names and return a set of valid names."""
    return {name.strip() for name in nodes_input.split(';') if name.strip()}


def parse_and_validate_edges(edges_input: str) -> list:
    """Parse a semi-colon-separated string of edges in the format (start_node,end_node) and return a list of tuples."""
    return [tuple(edge.strip('() ').split(',')) for edge in edges_input.split(';')]


def parse_and_validate_hyper_edges(edges_input: str) -> list:
    """Parse a semi-colon-separated string of hyper_edges in the format (node_1,node_2,...,node_n) and return a list of sets."""
    return [frozenset(edge.strip('() ').split(',')) for edge in edges_input.split(';')]
