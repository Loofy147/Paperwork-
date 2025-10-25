from csai.knowledge_base.knowledge_base import KnowledgeBase

class TemporalReasoningEngine:
    """
    Performs temporal reasoning to answer questions about time and sequence.
    """
    def __init__(self, knowledge_base: KnowledgeBase):
        """
        Initializes the TemporalReasoningEngine.

        Args:
            knowledge_base (KnowledgeBase): The knowledge base to reason over.
        """
        self.kb = knowledge_base

    def find_events_after(self, event_id: str) -> list:
        """
        Finds all events that occurred after a given event.

        Args:
            event_id (str): The ID of the event to query.

        Returns:
            list: A list of event IDs that occurred after the given event.
        """
        target_event = self.kb.get_node(event_id)
        if not target_event or "end_time" not in target_event:
            return []

        target_end_time = target_event["end_time"]

        events_after = []
        for node_id, properties in self.kb.graph.nodes(data=True):
            if properties.get("type") == "event" and "start_time" in properties:
                if properties["start_time"] > target_end_time:
                    events_after.append(node_id)

        return sorted(events_after, key=lambda eid: self.kb.get_node(eid)["start_time"])
