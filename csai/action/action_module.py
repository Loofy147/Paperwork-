class ActionModule:
    """Translates reasoned output into natural language responses.

    This module uses a template-based approach to generate human-readable
    answers from the structured results provided by the ReasoningEngine. It
    is responsible for the final step in the CSAI system's query processing
    pipeline, converting structured data back into a conversational format.
    """

    def generate_response(self, parsed_query: dict, results: list) -> str:
        """Generates a natural language response from a parsed query and a list of results.

        This method takes the original structured query and the results from the
        ReasoningEngine and constructs a human-readable response. The response
        format is determined by the query type and the results.

        Args:
            parsed_query (dict): The original structured query from the
                PerceptionModule. This dictionary contains details about the
                question being asked, such as the subject and the type of query.
            results (list): The list of results from the ReasoningEngine. This
                list contains the answers to the query, which will be formatted
                into a natural language response.

        Returns:
            str: A human-readable, natural language response that answers the
                 original question.
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
