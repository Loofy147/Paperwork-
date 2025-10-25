class ActionModule:
    """Translates reasoned output into natural language responses.

    This module uses a template-based approach to generate human-readable
    answers from the structured results provided by the ReasoningEngine. It
    is responsible for the final step in the CSAI system's query processing
    pipeline, converting structured data back into a conversational format.
    """
    def format_plan(self, plan: list) -> str:
        """
        Formats a plan into a human-readable string.

        Args:
            plan (list): A list of action IDs.

        Returns:
            str: A formatted string representing the plan.
        """
        if not plan:
            return "No plan is needed."

        formatted_plan = "Here is the plan:\n"
        for i, action_id in enumerate(plan):
            action_name = action_id.replace("action_", "").replace("_", " ")
            formatted_plan += f"{i+1}. {action_name}\n"
        return formatted_plan

    def generate_response(self, parsed_query: dict, results: list) -> str:
        """Generates a natural language response from a parsed query and a list
        of results.

        This method takes the original structured query and the results from
        the ReasoningEngine and constructs a human-readable response. The
        response format is determined by the query type and the results.

        Args:
            parsed_query (dict): The original structured query from the
                PerceptionModule. This dictionary contains details about the
                question being asked, such as the subject and type of query.
            results (list): The list of results from the ReasoningEngine. This
                list contains the answers to the query, which will be
                formatted into a natural language response.

        Returns:
            str: A human-readable, natural language response that answers the
                 original question.
        """
        subject = parsed_query.get("subject") # Use .get() for safety

        if parsed_query["type"] == "causal_explanation":
            event_name = parsed_query['event'].replace('_', ' ')
            if results:
                causes = " or ".join(sorted(list(set([cause.replace('_event_1', '').replace('_on', '').replace('_', ' ') for cause in results]))))
                return f"The {event_name} is caused by {causes}."
            else:
                return f"I'm sorry, I don't know why the {event_name}."

        if parsed_query["type"] == "temporal_question":
            if results:
                event_names = [event.replace("_event_1", "") for event in results]
                return f"After the {parsed_query['event'].replace('_event_1', '')}, the following events occurred: {', '.join(event_names)}."
            else:
                return f"I'm sorry, I don't know what happened after the {parsed_query['event'].replace('_event_1', '')}."

        if parsed_query["type"] == "counterfactual":
            intervention = parsed_query["intervention"]
            original_causes = set(results["original_causes"])
            counterfactual_causes = set(results["counterfactual_causes"])
            target_event = results["target_event"].replace("_", " ")
            removed_event = intervention["original_event"] # Use the original event for the response

            if not original_causes:
                return f"The {target_event} was not happening in the first place."

            if not counterfactual_causes:
                return f"If it had not {removed_event}, the {target_event} would not have occurred."

            if counterfactual_causes != original_causes:
                remaining_causes = " or ".join(sorted(list(set([cause.replace('_event_1', '').replace('_on', '').replace('_', ' ') for cause in counterfactual_causes]))))
                return f"If it had not {removed_event}, the {target_event} would still have occurred, but it would only be caused by {remaining_causes}."

            else: # counterfactual_causes == original_causes
                return "The outcome would not have changed."

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
