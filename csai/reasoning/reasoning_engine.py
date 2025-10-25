import time
from csai.knowledge_base.knowledge_base import KnowledgeBase

class ReasoningEngine:
    """
    Performs logical inference on a structured query using a knowledge base.

    This engine uses a simple forward-chaining approach to infer new facts
    from the knowledge base, with a focus on handling transitive 'is_a'
    relationships.
    """
    def __init__(self, knowledge_base: KnowledgeBase):
        """
        Initializes the ReasoningEngine with a reference to a KnowledgeBase.

        Args:
            knowledge_base (KnowledgeBase): The knowledge base to reason over.
        """
        self.kb = knowledge_base

    def execute_query(self, parsed_query: dict, deadline: float = 1.0) -> tuple[list, set | None]:
        """
        Executes a structured query against the knowledge base.

        Args:
            parsed_query (dict): The structured query from the PerceptionModule.
            deadline (float): The maximum time in seconds to spend on the query.

        Returns:
            tuple[list, set | None]: A tuple containing the list of results and,
                                     in case of a timeout, a set of partial results.
                                     Returns None for partial_results otherwise.
        """
        start_time = time.time()
        subject = parsed_query["subject"]

        if parsed_query["type"] == "has_property":
            edges = self.kb.find_edges(source_id=subject, label="has_property")
            # This query is simple and not expected to time out, so no deadline check.
            for _, o, _ in edges:
                node = self.kb.get_node(o)
                if node and node.get("type") == parsed_query["property"]:
                    return [o], None
            return [], None

        if parsed_query["type"] in ["is_a_specific", "is_a_generic"]:
            all_found_types = set()
            queue = [subject]
            processed = {subject}

            while queue:
                if time.time() - start_time > deadline:
                    return [], all_found_types

                current = queue.pop(0)
                edges = self.kb.find_edges(source_id=current, label="is_a")
                for _, target_node, _ in edges:
                    if target_node not in processed:
                        all_found_types.add(target_node)
                        queue.append(target_node)
                        processed.add(target_node)

            if parsed_query["type"] == "is_a_specific":
                final_results = [t for t in all_found_types if t == parsed_query["target"]]
                return final_results, None
            else:
                return sorted(list(all_found_types)), None

        if parsed_query["type"] == "has_part":
            # First, find all types of the subject.
            all_found_types = {subject}
            queue = [subject]
            processed = {subject}
            while queue:
                if time.time() - start_time > deadline:
                    return [], set() # Timed out while just finding types

                current = queue.pop(0)
                edges = self.kb.find_edges(source_id=current, label="is_a")
                for _, target_node, _ in edges:
                    if target_node not in processed:
                        all_found_types.add(target_node)
                        queue.append(target_node)
                        processed.add(target_node)

            # Now, check for the part in the subject and all its types.
            for t in all_found_types:
                if time.time() - start_time > deadline:
                    # Return empty-handed, as we didn't finish searching.
                    # A more complex implementation could return partial findings here.
                    return [], {"..."}

                edges = self.kb.find_edges(source_id=t, label="has_part")
                for _, part, _ in edges:
                    if part == parsed_query["part"]:
                        return [part], None # Found it!

            return [], None # Finished searching, didn't find it.

        return [], None
