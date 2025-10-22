import re
import spacy

class PerceptionModule:
    """Translates natural language queries into a structured, machine-readable format."""
    def __init__(self):
        try:
            self.nlp = spacy.load("en_core_web_sm", disable=["parser", "ner"])
        except OSError:
            from spacy.cli import download
            download("en_core_web_sm")
            self.nlp = spacy.load("en_core_web_sm", disable=["parser", "ner"])

    def parse_query(self, text):
        text = text.lower().strip()

        match = re.match(r"what type of ([\w_]+) is (?:a|an) ([\w_]+)\??", text)
        if match:
            return {"type": "is_a_specific", "subject": match.group(2), "target": match.group(1)}

        match = re.match(r"what is (?:a|an) ([\w_]+)\??", text)
        if match:
            return {"type": "is_a_generic", "subject": match.group(1)}

        match = re.match(r"what ([\w_]+) is (?:a|an) ([\w_]+)\??", text)
        if match:
            return {"type": "has_property", "subject": match.group(2), "property": self.nlp(match.group(1))[0].lemma_}

        return None
