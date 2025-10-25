import json
from csai.knowledge_base.knowledge_base import KnowledgeBase
from csai.perception.perception import PerceptionModule
from csai.reasoning.reasoning_engine import ReasoningEngine
from csai.reasoning.causal_reasoning_engine import CausalReasoningEngine
from csai.reasoning.counterfactual_reasoning_engine import CounterfactualReasoningEngine
from csai.action.action_module import ActionModule
from csai.learning.knowledge_acquirer import KnowledgeAcquirer
from csai.grounding.visual_grounder import VisualGrounder
from csai.reasoning.temporal_reasoning_engine import TemporalReasoningEngine
from csai.planning.planner import Planner
from csai.dialogue.dialogue_manager import DialogueManager

class CSAISystem:
    """
    The main Causal-Symbolic AI system.

    This class orchestrates the interaction between the Perception, Reasoning,
    and Action modules to answer commonsense questions.
    """
    def __init__(self, knowledge_base_path="knowledge_base.json"):
        """
        Initializes the CSAISystem and loads the knowledge base.

        Args:
            knowledge_base_path (str, optional): The path to the knowledge base
                                                 JSON file. Defaults to "knowledge_base.json".
        """
        self.kb = KnowledgeBase()
        self.perception = PerceptionModule(self.kb)
        self.reasoning = ReasoningEngine(self.kb)
        self.causal_reasoning = CausalReasoningEngine(self.kb)
        self.counterfactual_reasoning = CounterfactualReasoningEngine(self.kb)
        self.temporal_reasoning = TemporalReasoningEngine(self.kb)
        self.planner = Planner(self.kb)
        self.action = ActionModule()
        self.knowledge_acquirer = KnowledgeAcquirer(self.kb)
        self.visual_grounder = VisualGrounder()
        self.dialogue_manager = DialogueManager()
        self.current_state = {"sprinkler_off", "wet_grass"} # Initial state
        self._load_kb(knowledge_base_path)

    def _load_kb(self, path: str):
        """
        Loads the knowledge base from a JSON file.

        Args:
            path (str): The path to the JSON knowledge base file.
        """
        with open(path, 'r') as f:
            data = json.load(f)

        for node in data["nodes"]:
            self.kb.add_node(node["id"], **node["properties"])

        for edge in data["edges"]:
            self.kb.add_edge(edge["source"], edge["target"], edge["label"])

    def ask(self, question: str, deadline: float = 1.0) -> str:
        """
        Asks a question to the CSAI system.

        This method takes a natural language question, parses it, executes a
        query against the knowledge base, and returns a natural language response.

        Args:
            question (str): The natural language question to ask.
            deadline (float): The maximum time in seconds to spend on the query.

        Returns:
            str: The natural language answer.
        """
        parsed_query = self.perception.parse_query(question)
        if not parsed_query:
            return "I'm sorry, I don't understand your question."

        if parsed_query["type"] == "causal_explanation":
            results, partial_results = self.causal_reasoning.explain_event(parsed_query["event"], deadline)
        elif parsed_query["type"] == "counterfactual":
            results, partial_results = self.counterfactual_reasoning.evaluate(parsed_query["intervention"], deadline)
        elif parsed_query["type"] == "temporal_question":
            results = self.temporal_reasoning.find_events_after(parsed_query["event"])
            partial_results = None
        else:
            results, partial_results = self.reasoning.execute_query(parsed_query, deadline)

        parsed_query["partial_results"] = partial_results
        return self.action.generate_response(parsed_query, results)

    def plan(self, goal: str, chosen_method: str = None) -> str:
        """
        Generates a plan to achieve a given goal, engaging in a dialogue if needed.

        Args:
            goal (str): The goal to achieve.
            chosen_method (str, optional): The method chosen by the user.

        Returns:
            str: A message indicating the plan, a question, or the result.
        """
        result = self.planner.find_plan(self.current_state, goal, chosen_method)

        if isinstance(result, list): # A concrete plan was found
            return self.action.format_plan(result)
        elif isinstance(result, dict): # The planner needs a choice
            return self.dialogue_manager.start_clarification(result)
        elif chosen_method: # An invalid choice was made
            return "Invalid choice. Please try again."
        else:
            return "I'm sorry, I couldn't find a plan to achieve that goal."

    def learn(self, file_path: str) -> str:
        """
        Learns new facts from a text file.

        Args:
            file_path (str): The path to the text file.

        Returns:
            str: A message indicating the result of the learning process.
        """
        try:
            with open(file_path, 'r') as f:
                text = f.read()
            self.knowledge_acquirer.learn_from_text(text)
            return "I have learned new facts from the text."
        except FileNotFoundError:
            return "I'm sorry, I couldn't find that file."

    def ground(self, concept_name: str, image_directory: str) -> str:
        """
        Grounds a concept in an image.

        Args:
            concept_name (str): The name of the concept to ground.
            image_directory (str): The path to the directory of images.

        Returns:
            str: A message indicating the result of the grounding process.
        """
        best_image = self.visual_grounder.ground_concept(concept_name, image_directory)
        if best_image:
            return f"I believe the best image for '{concept_name}' is '{best_image}'."
        else:
            return f"I'm sorry, I couldn't find a suitable image for '{concept_name}' in that directory."
