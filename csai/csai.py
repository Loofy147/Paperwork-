from csai.knowledge_base.knowledge_base import KnowledgeBase
from csai.perception.perception import PerceptionModule
from csai.reasoning.reasoning_engine import ReasoningEngine
from csai.action.action_module import ActionModule

class CSAISystem:
    """The main Causal-Symbolic AI system."""
    def __init__(self):
        self.kb = KnowledgeBase()
        self.perception = PerceptionModule()
        self.reasoning = ReasoningEngine(self.kb)
        self.action = ActionModule()
        self._populate_kb()

    def _populate_kb(self):
        self.kb.add_node("raven", name="raven"); self.kb.add_node("crow", name="crow"); self.kb.add_node("canary", name="canary")
        self.kb.add_node("bird", name="bird"); self.kb.add_node("animal", name="animal"); self.kb.add_node("living_thing", name="living_thing")
        self.kb.add_node("black", name="black", type="color"); self.kb.add_node("yellow", name="yellow", type="color")
        self.kb.add_edge("raven", "bird", "is_a"); self.kb.add_edge("crow", "bird", "is_a"); self.kb.add_edge("canary", "bird", "is_a")
        self.kb.add_edge("bird", "animal", "is_a"); self.kb.add_edge("animal", "living_thing", "is_a")
        self.kb.add_edge("raven", "black", "has_property"); self.kb.add_edge("crow", "black", "has_property"); self.kb.add_edge("canary", "yellow", "has_property")

    def ask(self, question):
        parsed_query = self.perception.parse_query(question)
        if not parsed_query:
            return "I'm sorry, I don't understand your question."

        results = self.reasoning.execute_query(parsed_query)
        return self.action.generate_response(parsed_query, results)
