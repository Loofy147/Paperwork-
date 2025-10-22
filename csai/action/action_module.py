class ActionModule:
    """Translates the reasoned output back into a natural language response."""
    def generate_response(self, parsed_query, results):
        if not results:
            return "I'm sorry, I don't have an answer to that question."

        subject = parsed_query["subject"]
        if parsed_query["type"] == "has_property":
            return f"A {subject} is {results[0]}."

        if parsed_query["type"] == "is_a_specific":
            return f"A {subject} is a type of {results[0]}."

        if parsed_query["type"] == "is_a_generic":
            return f"A {subject} is a type of {', '.join(results)}."
