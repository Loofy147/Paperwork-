import networkx as nx

class KnowledgeBase:
    """A graph-based knowledge base for storing commonsense knowledge."""
    def __init__(self):
        self.graph = nx.DiGraph()

    def add_node(self, node_id, **properties):
        self.graph.add_node(node_id, **properties)

    def add_edge(self, source, target, label):
        self.graph.add_edge(source, target, label=label)

    def get_node(self, node_id):
        return self.graph.nodes.get(node_id)

    def find_edges(self, source_id=None, label=None):
        return [
            (u, v, d['label'])
            for u, v, d in self.graph.edges(data=True)
            if (source_id is None or u == source_id) and (label is None or d['label'] == label)
        ]
