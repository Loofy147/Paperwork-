import time
import copy
from csai.knowledge_base.knowledge_base import KnowledgeBase
from csai.reasoning.causal_reasoning_engine import CausalReasoningEngine

class CounterfactualReasoningEngine:
    """
    Performs counterfactual reasoning to answer 'what if' questions by simulating
    interventions on a copy of the knowledge graph.
    """

    def __init__(self, knowledge_base: KnowledgeBase):
        """
        Initializes the CounterfactualReasoningEngine.

        Args:
            knowledge_base (KnowledgeBase): The base knowledge base to use for reasoning.
        """
        self.kb = knowledge_base
        # The engine uses a CausalReasoningEngine to evaluate outcomes.
        self.causal_engine = CausalReasoningEngine(self.kb)

    def evaluate(self, intervention: dict, deadline: float = 1.0) -> tuple[dict, set | None]:
        """
        Evaluates a counterfactual query.

        Args:
            intervention (dict): A dictionary describing the intervention.
            deadline (float): The maximum time in seconds for the query.

        Returns:
            tuple[dict, set | None]: A tuple containing the result dictionary and
                                     potential partial results on timeout.
        """
        start_time = time.time()

        # 1. Create a temporary copy of the knowledge base to modify.
        temp_kb = KnowledgeBase()
        temp_kb.graph = copy.deepcopy(self.kb.graph)

        # The causal engine must reason over the *temporary* knowledge base.
        temp_causal_engine = CausalReasoningEngine(temp_kb)

        # 2. Apply the intervention to the temporary graph.
        if intervention["type"] == "remove_cause":
            event_to_remove = intervention["event"]
            if temp_kb.graph.has_node(event_to_remove):
                temp_kb.graph.remove_node(event_to_remove)

        if time.time() - start_time > deadline:
            return {"outcome": "timeout"}, {"..."}

        # 3. Re-evaluate the target event in the modified graph.
        target_event = intervention["target_event"]

        # First, check the original outcome.
        original_causes, _ = self.causal_engine.explain_event(target_event)

        # Then, check the outcome in the counterfactual world.
        counterfactual_causes, _ = temp_causal_engine.explain_event(target_event)

        result = {
            "original_causes": original_causes,
            "counterfactual_causes": counterfactual_causes,
            "target_event": target_event
        }

        return result, None
