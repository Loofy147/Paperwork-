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
        subject = parsed_query.get("subject") # Use .get() for safety

        if parsed_query["type"] == "causal_explanation":
            event_name = parsed_query['event'].replace('_', ' ')
            if results:
                causes = " or ".join([cause.replace('_', ' ') for cause in results])
                return f"The {event_name} is caused by {causes}."
            else:
                return f"I'm sorry, I don't know why the {event_name}."

        partial_results = parsed_query.get("partial_results")

        if partial_results is not None: # Timeout occurred
            if partial_results:
                return f"A {subject} is a type of {', '.join(sorted(list(partial_results)))}."
            else:
                return "I started searching, but the deadline was too short to find any results."

        if not results: # No timeout, but no results found
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
