from csai.knowledge_base.knowledge_base import KnowledgeBase


class ReasoningEngine:
    """Performs logical inference on a structured query using a knowledge base.

    This engine uses a simple forward-chaining approach to infer new facts
    from the knowledge base, with a focus on handling transitive 'is_a'
    relationships. It is the core of the CSAI system, responsible for
    deriving answers to user queries by traversing the knowledge graph.
    """

    def __init__(self, knowledge_base: KnowledgeBase):
        """Initializes the ReasoningEngine with a reference to a KnowledgeBase.

        Args:
            knowledge_base (KnowledgeBase): The knowledge base to reason over.
        """
        self.kb = knowledge_base

    def execute_query(self, parsed_query: dict) -> list:
        """Executes a structured query against the knowledge base.

        This method takes a structured query from the PerceptionModule and
        returns a list of results. The reasoning process depends on the type
        of query. For 'is_a' queries, it performs a breadth-first search to
        find all supertypes of a given subject. For 'has_part' queries, it
        finds all parts of a subject, including inherited parts from its
        supertypes.

        Args:
            parsed_query (dict): The structured query from the
                PerceptionModule.

        Returns:
            list: A list of results that satisfy the query. The format of the
                  results depends on the query type.
        """
        query_type = parsed_query["type"]
        subject = parsed_query["subject"]

        if query_type == "has_property":
            edges = self.kb.find_edges(source_id=subject, label="has_property")
            for _, o, _ in edges:
                node = self.kb.get_node(o)
                if node and node.get("type") == parsed_query["property"]:
                    return [o]
            return []

        if query_type in ["is_a_specific", "is_a_generic"]:
            inferred_types = self._find_supertypes(subject)
            if query_type == "is_a_specific":
                target = parsed_query["target"]
                return [t for t in inferred_types if t == target]
            else:
                return sorted(list(inferred_types))

        if query_type == "has_part":
            inferred_parts = set()
            inferred_types = self._find_supertypes(subject)
            inferred_types.add(subject)
            for t in inferred_types:
                edges = self.kb.find_edges(source_id=t, label="has_part")
                for _, o, _ in edges:
                    inferred_parts.add(o)
            return [p for p in inferred_parts if p == parsed_query["part"]]

        return []

    def _find_supertypes(self, subject: str) -> set:
        """Finds all supertypes of a subject using a breadth-first search."""
        inferred_types = {subject}
        queue = [subject]
        while queue:
            current = queue.pop(0)
            edges = self.kb.find_edges(source_id=current, label="is_a")
            for _, o, _ in edges:
                if o not in inferred_types:
                    inferred_types.add(o)
                    queue.append(o)
        inferred_types.remove(subject)
        return inferred_types
