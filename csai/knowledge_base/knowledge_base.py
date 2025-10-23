import networkx as nx

class KnowledgeBase:
    """
    A graph-based knowledge base for storing and retrieving commonsense knowledge.

    This class uses a networkx DiGraph to represent the knowledge base, where
    nodes are concepts and edges are relationships between them.
    """
    def __init__(self):
        """Initializes the KnowledgeBase."""
        self.graph = nx.DiGraph()

    def add_node(self, node_id, **properties):
        """
        Adds a node to the knowledge base.

        Args:
            node_id (str): The unique identifier for the node.
            **properties: Arbitrary keyword arguments representing node properties.
        """
        self.graph.add_node(node_id, **properties)

    def add_edge(self, source, target, label):
        """
        Adds a directed edge between two nodes in the knowledge base.

        Args:
            source (str): The identifier of the source node.
            target (str): The identifier of the target node.
            label (str): The label of the relationship (e.g., 'is_a', 'has_property').
        """
        self.graph.add_edge(source, target, label=label)

    def get_node(self, node_id):
        """
        Retrieves a node and its properties by its ID.

        Args:
            node_id (str): The identifier of the node to retrieve.

        Returns:
            dict or None: A dictionary of the node's properties, or None if not found.
        """
        return self.graph.nodes.get(node_id)

    def find_edges(self, source_id=None, label=None):
        """
        Finds edges in the knowledge base that match the given criteria.

        Args:
            source_id (str, optional): The source node of the edges to find. Defaults to None.
            label (str, optional): The label of the edges to find. Defaults to None.

        Returns:
            list: A list of tuples, where each tuple represents an edge
                  (source, target, label).
        """
        return [
            (u, v, d['label'])
            for u, v, d in self.graph.edges(data=True)
            if (source_id is None or u == source_id) and (label is None or d['label'] == label)
        ]

    def find_incoming_edges(self, target_id, label=None):
        """
        Finds incoming edges to a specific node.

        Args:
            target_id (str): The target node of the edges to find.
            label (str, optional): The label of the edges to find. Defaults to None.

        Returns:
            list: A list of tuples, where each tuple represents an edge
                  (source, target, label).
        """
        if not self.graph.has_node(target_id):
            return []

        return [
            (u, v, d['label'])
            for u, v, d in self.graph.in_edges(target_id, data=True)
            if label is None or d['label'] == label
        ]
