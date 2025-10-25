import time
from csai.knowledge_base.knowledge_base import KnowledgeBase

class CausalReasoningEngine:
    """
    Performs causal inference to answer 'why' questions.

    This engine traverses the knowledge graph to find causal chains that
    explain a given event or state.
    """
    def __init__(self, knowledge_base: KnowledgeBase):
        """
        Initializes the CausalReasoningEngine with a reference to a KnowledgeBase.

        Args:
            knowledge_base (KnowledgeBase): The knowledge base to reason over.
        """
        self.kb = knowledge_base

    def explain_event(self, event: str, deadline: float = 1.0) -> tuple[list, set | None]:
        """
        Finds the direct causes of a given event.

        Args:
            event (str): The event or state to be explained (e.g., 'wet_grass').
            deadline (float): The maximum time in seconds to spend on the query.

        Returns:
            tuple[list, set | None]: A tuple containing a list of causes and,
                                     in case of a timeout, a set of partial results.
                                     Returns None for partial_results otherwise.
        """
        start_time = time.time()

        # Find all incoming edges with the 'causes' label to the event node.
        edges = self.kb.find_incoming_edges(target_id=event, label="causes")

        causes = []
        for source, _, _ in edges:
            if time.time() - start_time > deadline:
                return [], set(causes) # Return partial results on timeout
            causes.append(source)

        return sorted(causes), None
