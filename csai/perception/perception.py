import re
import spacy

class PerceptionModule:
    """Translates natural language queries into a structured, machine-readable format.

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
            dict or None: A dictionary representing the structured query,
                          or None if the query does not match any known patterns.
                          The dictionary contains the query type and its
                          parameters.
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

        return None
