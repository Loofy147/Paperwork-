class ActionModule:
    """
    Translates the reasoned output back into a natural language response.

    This module uses a template-based approach to generate human-readable
    answers from the structured results provided by the ReasoningEngine.
    """
    def generate_response(self, parsed_query: dict, results: list) -> str:
        """
        Generates a natural language response from a parsed query and a list of results.

        Args:
            parsed_query (dict): The original structured query.
            results (list): The list of results from the ReasoningEngine.

        Returns:
            str: A human-readable, natural language response.
        """
        subject = parsed_query["subject"]

        if not results:
            if parsed_query["type"] == "has_part":
                return f"No, a {subject} does not have {parsed_query['part']}."
            return "I'm sorry, I don't have an answer to that question."

        if parsed_query["type"] == "has_property":
            return f"A {subject} is {results[0]}."

        if parsed_query["type"] == "is_a_specific":
            return f"A {subject} is a type of {results[0]}."

        if parsed_query["type"] == "is_a_generic":
            return f"A {subject} is a type of {', '.join(results)}."

        if parsed_query["type"] == "has_part":
            return f"Yes, a {subject} has {results[0]}."
