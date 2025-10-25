import networkx as nx


class KnowledgeBase:
    """A graph-based knowledge base for storing and retrieving commonsense
    knowledge.

    This class uses a networkx DiGraph to represent the knowledge base, where
    nodes are concepts and edges are relationships between them. It provides
    a set of methods for adding, retrieving, and querying the knowledge graph.
    The graph is stored in memory and can be loaded from a JSON file.
    """

    def __init__(self):
        """Initializes the KnowledgeBase.

        This constructor initializes an empty networkx DiGraph, which will be
        used to store the knowledge base.
        """
        self.graph = nx.DiGraph()

    def add_node(self, node_id, **properties):
        """Adds a node to the knowledge base.

        This method adds a new node to the knowledge graph with a unique
        identifier and a set of optional properties.

        Args:
            node_id (str): The unique identifier for the node. This is used
                to reference the node in other parts of the knowledge base.
            **properties: Arbitrary keyword arguments representing node
                properties. These can be used to store additional information
                about the node, such as its type or attributes.
        """
        self.graph.add_node(node_id, **properties)

    def add_edge(self, source, target, label):
        """Adds a directed edge between two nodes in the knowledge base.

        This method creates a directed edge from a source node to a target node
        with a given label. The label represents the relationship between the
        two nodes.

        Args:
            source (str): The identifier of the source node.
            target (str): The identifier of the target node.
            label (str): The label of the relationship (e.g., 'is_a',
                'has_property').
        """
        self.graph.add_edge(source, target, label=label)

    def get_node(self, node_id):
        """Retrieves a node and its properties by its ID.

        This method returns the properties of a node in the knowledge graph
        based on its unique identifier.

        Args:
            node_id (str): The identifier of the node to retrieve.

        Returns:
            dict or None: A dictionary of the node's properties, or None if
                          the node is not found.
        """
        return self.graph.nodes.get(node_id)

    def find_edges(self, source_id=None, label=None):
        """Finds edges in the knowledge base that match the given criteria.

        This method searches the knowledge graph for edges that match the
        specified source node and/or label. If no criteria are provided, it
        returns all edges in the graph.

        Args:
            source_id (str, optional): The source node of the edges to find.
                Defaults to None.
            label (str, optional): The label of the edges to find. Defaults
                to None.

        Returns:
            list: A list of tuples, where each tuple represents an edge
                  (source, target, label).
        """
        return [
            (u, v, d['label'])
            for u, v, d in self.graph.edges(data=True)
            if (source_id is None or u == source_id) and
               (label is None or d['label'] == label)
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
