import json
from csai.knowledge_base.knowledge_base import KnowledgeBase
from csai.perception.perception import PerceptionModule
from csai.reasoning.reasoning_engine import ReasoningEngine
from csai.action.action_module import ActionModule

class CSAISystem:
    """The main Causal-Symbolic AI system.

    This class orchestrates the interaction between the Perception, Reasoning,
    and Action modules to answer commonsense questions. It is the entry point
    for the CSAI system, and it manages the overall query processing pipeline.
    """

    def __init__(self, knowledge_base_path="knowledge_base.json"):
        """Initializes the CSAISystem and loads the knowledge base.

        This constructor initializes all the modules of the CSAI system and
        loads the knowledge base from a JSON file.

        Args:
            knowledge_base_path (str, optional): The path to the knowledge base
                                                 JSON file. Defaults to
                                                 "knowledge_base.json".
        """
        self.kb = KnowledgeBase()
        self.perception = PerceptionModule()
        self.reasoning = ReasoningEngine(self.kb)
        self.action = ActionModule()
        self._load_kb(knowledge_base_path)

    def _load_kb(self, path: str):
        """Loads the knowledge base from a JSON file.

        This private method reads a JSON file containing the knowledge base
        and populates the KnowledgeBase object with nodes and edges.

        Args:
            path (str): The path to the JSON knowledge base file.
        """
        with open(path, 'r') as f:
            data = json.load(f)

        for node in data["nodes"]:
            self.kb.add_node(node["id"], **node["properties"])

        for edge in data["edges"]:
            self.kb.add_edge(edge["source"], edge["target"], edge["label"])

    def ask(self, question: str) -> str:
        """Asks a question to the CSAI system.

        This method takes a natural language question, parses it, executes a
        query against the knowledge base, and returns a natural language
        response. It is the main method for interacting with the CSAI system.

        Args:
            question (str): The natural language question to ask.

        Returns:
            str: The natural language answer.
        """
        parsed_query = self.perception.parse_query(question)
        if not parsed_query:
            return "I'm sorry, I don't understand your question."

        results = self.reasoning.execute_query(parsed_query)
        return self.action.generate_response(parsed_query, results)
