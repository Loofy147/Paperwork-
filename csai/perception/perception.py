import re
import spacy


class PerceptionModule:
    """Translates natural language queries into a structured format.

    This module uses a series of regular expressions to parse common question
    formats and convert them into a structured dictionary that can be used by
    the ReasoningEngine. It is the first step in the CSAI system's query
    processing pipeline, responsible for understanding the user's intent.
    """

    def __init__(self):
        """Initializes the PerceptionModule and loads the spacy model.

        This constructor loads the `en_core_web_sm` spacy model, which is used
        for lemmatization. If the model is not found, it is automatically
        downloaded. The parser and named entity recognizer are disabled to
        improve performance.
        """
    def __init__(self, knowledge_base):
        """Initializes the PerceptionModule and loads the spacy model."""
        self.kb = knowledge_base
        try:
            self.nlp = spacy.load("en_core_web_sm", disable=["parser", "ner"])
        except OSError:
            from spacy.cli import download
            download("en_core_web_sm")
            self.nlp = spacy.load("en_core_web_sm", disable=["parser", "ner"])

    def parse_query(self, text):
        """Parses a natural language query into a structured dictionary.

        This method takes a natural language query as input and attempts to
        match it against a set of predefined patterns. If a match is found,
        it returns a dictionary containing the structured representation of
        the query. Otherwise, it returns None.

        Args:
            text (str): The natural language query to parse.

        Returns:
            A dictionary representing the structured query, or None if
            the query does not match any known patterns. The dictionary
            contains the query type and its parameters.
        """
        text = text.lower().strip()

        # Pattern 1: "What type of [Target] is a/an [Subject]?"
        match = re.match(r"what type of ([\w_]+) is (?:a|an) ([\w_]+)\??", text)
        if match:
            return {"type": "is_a_specific",
                    "subject": match.group(2),
                    "target": match.group(1)}

        # Pattern 2: "What is a/an [Subject]?"
        match = re.match(r"what is (?:a|an) ([\w_]+)\??", text)
        if match:
            return {"type": "is_a_generic", "subject": match.group(1)}

        # Pattern 3: "What [Property] is a/an [Subject]?"
        match = re.match(r"what ([\w_]+) is (?:a|an) ([\w_]+)\??", text)
        if match:
            prop = self.nlp(match.group(1))[0].lemma_
            return {"type": "has_property",
                    "subject": match.group(2),
                    "property": prop}

        # Pattern 4: "Does a [Subject] have [Part]?"
        match = re.match(r"does (?:a|an) ([\w_]+) have ([\w_]+)\??", text)
        if match:
            return {"type": "has_part",
                    "subject": match.group(1),
                    "part": match.group(2)}

        # Pattern 5: "Why is the [Subject] [State]?"
        match = re.match(r"why is the ([\w_]+) ([\w_]+)\??", text)
        if match:
            subject = match.group(1)
            state = match.group(2)
            event_id = f"{state}_{subject}"
            return {"type": "causal_explanation", "event": event_id}

        # Pattern 6: "What happened after the [event]?"
        match = re.match(r"what happened after the ([\w_]+)\??", text)
        if match:
            event_name = match.group(1)
            # Find the event in the KB that matches the name
            for node_id, props in self.kb.graph.nodes(data=True):
                if props.get("name") == event_name and props.get("type") == "event":
                    return {"type": "temporal_question", "event": node_id}
            return None # Event not found

        # Pattern 7: "What would happen to the [target] if it had not [event]?"
        match = re.match(r"what would happen to the ([\w\s]+) if it had not ([\w_]+)\??", text)
        if match:
            target_phrase = match.group(1).strip()
            target_id = target_phrase.replace(" ", "_")
            original_event = match.group(2)
            lemmatized_event = self.nlp(original_event)[0].lemma_
            return {
                "type": "counterfactual",
                "intervention": {
                    "type": "remove_cause",
                    "event": lemmatized_event,
                    "original_event": original_event,
                    "target_event": target_id
                }
            }

        # Pattern 8: "plan for [goal]"
        match = re.match(r"plan for ([\w\s]+)\??", text)
        if match:
            goal_phrase = match.group(1).strip()
            goal_id = goal_phrase.replace(" ", "_")
            return {"type": "plan", "goal": goal_id}

        return None
