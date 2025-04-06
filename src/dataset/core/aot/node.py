class AoTNode:
    """Base AoT node class with shared functionality."""
    def __init__(self, name, level, node_type):
        self.name = name
        self.level = level
        self.node_type = node_type
        self.children = []
        
    def insert(self, node):
        """Insert a child node."""
        self.children.append(node)

class RootNode(AoTNode):
    """Root node in the AoT."""
    def __init__(self, name):
        super().__init__(name, "Root", "or")

# Implement other node classes (StructureNode, ComponentNode, etc.)
