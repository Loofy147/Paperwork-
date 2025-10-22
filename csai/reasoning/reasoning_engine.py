from csai.knowledge_base.knowledge_base import KnowledgeBase

class ReasoningEngine:
    """Performs logical inference on a structured query using a knowledge base."""
    def __init__(self, knowledge_base):
        self.kb = knowledge_base

    def execute_query(self, parsed_query):
        subject = parsed_query["subject"]

        if parsed_query["type"] == "has_property":
            edges = self.kb.find_edges(source_id=subject, label="has_property")
            for _, o, _ in edges:
                node = self.kb.get_node(o)
                if node and node.get("type") == parsed_query["property"]:
                    return [o]
            return []

        if parsed_query["type"] in ["is_a_specific", "is_a_generic"]:
            inferred_types = {subject}
            queue = [subject]
            while queue:
                current = queue.pop(0)
                edges = self.kb.find_edges(source_id=current, label="is_a")
                for _, o, _ in edges:
                    if o not in inferred_types:
                        inferred_types.add(o)
                        queue.append(o)

            inferred_types.remove(subject) # Don't report that a raven is a raven

            if parsed_query["type"] == "is_a_specific":
                return [t for t in inferred_types if t == parsed_query["target"]]
            else:
                return sorted(list(inferred_types))

        return []
