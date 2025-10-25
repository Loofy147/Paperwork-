import spacy
from csai.knowledge_base.knowledge_base import KnowledgeBase

class KnowledgeAcquirer:
    """
    Learns new facts from unstructured text and adds them to a knowledge base.
    """
    def __init__(self, knowledge_base: KnowledgeBase):
        """
        Initializes the KnowledgeAcquirer.

        Args:
            knowledge_base (KnowledgeBase): The knowledge base to add new facts to.
        """
        self.kb = knowledge_base
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            from spacy.cli import download
            download("en_core_web_sm")
            self.nlp = spacy.load("en_core_web_sm")

    def learn_from_text(self, text: str):
        """
        Parses a block of text to extract new facts and add them to the knowledge base.

        This initial implementation focuses on extracting simple 'is_a' relationships.
        For example, from the sentence "A raven is a type of bird," it will extract
        the relationship (raven, is_a, bird).

        Args:
            text (str): The text to learn from.
        """
        doc = self.nlp(text)
        for sent in doc.sents:
            self._extract_is_a_relationships(sent)

    def _extract_is_a_relationships(self, sent):
        """
        Extracts 'is_a' relationships from a single sentence using dependency parsing.
        This version is more robust and handles articles (e.g., "a", "an").
        """
        for token in sent:
            # Find the root of the sentence, which is often the main verb.
            if token.dep_ == "ROOT" and token.lemma_ == "be":
                subject = None
                obj = None

                # Find the subject and object of the verb "be".
                for child in token.children:
                    if child.dep_ == "nsubj": # Nominal subject
                        subject = child
                    elif child.dep_ == "attr": # Attribute (the object in "is a")
                        obj = child

                if subject and obj:
                    # Find the actual nouns, skipping determiners like "a" or "an".
                    if subject.pos_ == "DET":
                        subject = next(subject.children, None)
                    if obj.pos_ == "DET":
                        obj = next(obj.children, None)

                    if subject and obj and subject.pos_ == "NOUN" and obj.pos_ == "NOUN":
                        subject_id = subject.text.lower().replace(" ", "_")
                        obj_id = obj.text.lower().replace(" ", "_")

                        if not self.kb.get_node(subject_id):
                            self.kb.add_node(subject_id, name=subject.text)
                        if not self.kb.get_node(obj_id):
                            self.kb.add_node(obj_id, name=obj.text)

                        self.kb.add_edge(subject_id, obj_id, "is_a")
