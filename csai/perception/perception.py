import re
import spacy
import sys


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
        for lemmatization. If the model is not found, it prints an error
        message and exits.
        """
        try:
            self.nlp = spacy.load("en_core_web_sm", disable=["parser", "ner"])
        except OSError:
            print(
                "Error: Spacy model 'en_core_web_sm' not found. "
                "Please run 'python -m spacy download en_core_web_sm' "
                "to download it."
            )
            sys.exit(1)

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
        parsers = [
            self._parse_is_a_specific,
            self._parse_is_a_generic,
            self._parse_has_property,
            self._parse_has_part,
        ]
        for parser in parsers:
            result = parser(text)
            if result:
                return result
        return None

    def _parse_is_a_specific(self, text):
        """Parses "What type of [Target] is a/an [Subject]?" queries."""
        pattern = r"what type of ([\w_]+) is (?:a|an) ([\w_]+)\??"
        match = re.match(pattern, text)
        if match:
            return {"type": "is_a_specific",
                    "subject": match.group(2),
                    "target": match.group(1)}
        return None

    def _parse_is_a_generic(self, text):
        """Parses "What is a/an [Subject]?" queries."""
        match = re.match(r"what is (?:a|an) ([\w_]+)\??", text)
        if match:
            return {"type": "is_a_generic", "subject": match.group(1)}
        return None

    def _parse_has_property(self, text):
        """Parses "What [Property] is a/an [Subject]?" queries."""
        match = re.match(r"what ([\w_]+) is (?:a|an) ([\w_]+)\??", text)
        if match:
            prop = self.nlp(match.group(1))[0].lemma_
            return {"type": "has_property",
                    "subject": match.group(2),
                    "property": prop}
        return None

    def _parse_has_part(self, text):
        """Parses "Does a [Subject] have [Part]?" queries."""
        match = re.match(r"does (?:a|an) ([\w_]+) have ([\w_]+)\??", text)
        if match:
            return {"type": "has_part",
                    "subject": match.group(1),
                    "part": match.group(2)}
        return None
