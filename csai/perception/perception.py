import re
import spacy

class PerceptionModule:
    """
    Translates natural language queries into a structured, machine-readable format.

    This module uses a series of regular expressions to parse common question
    formats and convert them into a structured dictionary that can be used by
    the ReasoningEngine.
    """
    def __init__(self):
        """Initializes the PerceptionModule and loads the spacy model."""
        try:
            self.nlp = spacy.load("en_core_web_sm", disable=["parser", "ner"])
        except OSError:
            from spacy.cli import download
            download("en_core_web_sm")
            self.nlp = spacy.load("en_core_web_sm", disable=["parser", "ner"])

    def parse_query(self, text):
        """
        Parses a natural language query into a structured dictionary.

        Args:
            text (str): The natural language query to parse.

        Returns:
            dict or None: A dictionary representing the structured query,
                          or None if the query does not match any known patterns.
        """
        text = text.lower().strip()

        # Pattern 1: "What type of [Target] is a/an [Subject]?"
        match = re.match(r"what type of ([\w_]+) is (?:a|an) ([\w_]+)\??", text)
        if match:
            return {"type": "is_a_specific", "subject": match.group(2), "target": match.group(1)}

        # Pattern 2: "What is a/an [Subject]?"
        match = re.match(r"what is (?:a|an) ([\w_]+)\??", text)
        if match:
            return {"type": "is_a_generic", "subject": match.group(1)}

        # Pattern 3: "What [Property] is a/an [Subject]?"
        match = re.match(r"what ([\w_]+) is (?:a|an) ([\w_]+)\??", text)
        if match:
            return {"type": "has_property", "subject": match.group(2), "property": self.nlp(match.group(1))[0].lemma_}

        # Pattern 4: "Does a [Subject] have [Part]?"
        match = re.match(r"does (?:a|an) ([\w_]+) have ([\w_]+)\??", text)
        if match:
            return {"type": "has_part", "subject": match.group(1), "part": match.group(2)}

        # Pattern 5: "Why is the [Subject] [State]?"
        match = re.match(r"why is the ([\w_]+) ([\w_]+)\??", text)
        if match:
            subject = match.group(1)
            state = match.group(2)
            event_id = f"{state}_{subject}"
            return {"type": "causal_explanation", "event": event_id}

        return None
