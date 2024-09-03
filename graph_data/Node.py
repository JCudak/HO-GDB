class Node:
    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return f"'{self.name}'"

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)
