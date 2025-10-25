from csai.knowledge_base.knowledge_base import KnowledgeBase

class Planner:
    """
    A Hierarchical Task Network (HTN) planner that can decompose abstract tasks
    into concrete plans.
    """

    def __init__(self, knowledge_base: KnowledgeBase):
        """
        Initializes the Planner.

        Args:
            knowledge_base (KnowledgeBase): The knowledge base to use for planning.
        """
        self.kb = knowledge_base

    def find_plan(self, current_state: set, goal: str, chosen_method: str = None) -> list | dict | None:
        """
        Finds a sequence of actions to achieve a goal.

        If multiple methods are available to achieve the goal, it will return a
        dictionary of choices for the user.

        Args:
            current_state (set): The current state of the world.
            goal (str): The goal to achieve.
            chosen_method (str, optional): The method chosen by the user.

        Returns:
            list, dict, or None: A list of actions, a dictionary of choices, or None.
        """
        # Find the abstract task that achieves the goal.
        task = self._find_task_for_goal(goal)
        if not task:
            return None

        # Find all valid methods for the task.
        valid_methods = [
            method for method in self._find_methods_for_task(task)
            if self._preconditions_met(current_state, self._get_preconditions(method))
        ]

        # If a method has been chosen, use it.
        if chosen_method:
            if chosen_method in valid_methods:
                return self._decompose_method(current_state, chosen_method)
            else:
                return None # Invalid choice

        # If there are multiple valid methods, ask the user to choose.
        if len(valid_methods) > 1:
            return {method: self.kb.get_node(method)["name"] for method in valid_methods}

        # If there is only one valid method, use it.
        if len(valid_methods) == 1:
            return self._decompose_method(current_state, valid_methods[0])

        return None

    def _decompose_method(self, current_state: set, method_id: str) -> list | None:
        """Decomposes a method into a sequence of actions."""
        preconditions = self._get_preconditions(method_id)
        if not self._preconditions_met(current_state, preconditions):
            return None

        subtasks = self._get_subtasks(method_id)
        plan = []
        for subtask in subtasks:
            if self.kb.get_node(subtask)["type"] == "action":
                plan.append(subtask)
            else:
                # Recursive decomposition of sub-methods
                sub_plan = self._decompose_method(current_state, subtask)
                if sub_plan:
                    plan.extend(sub_plan)
        return plan

    def _find_task_for_goal(self, goal: str) -> str | None:
        """Finds the abstract task that can achieve a given goal."""
        for u, v, label in self.kb.graph.edges(data="label"):
            if label == "has_add_effect" and v == goal:
                action = u
                for t, a, label2 in self.kb.graph.in_edges(action, data="label"):
                    if label2 == "has_subtask":
                        method = t
                        for task, m, label3 in self.kb.graph.in_edges(method, data="label"):
                            if label3 == "decomposes":
                                return task
        return None

    def _find_methods_for_task(self, task_id: str) -> list:
        """Finds all methods that can decompose a given task."""
        return [v for u, v, label in self.kb.find_edges(source_id=task_id) if label == "decomposes"]

    def _get_preconditions(self, method_id: str) -> set:
        """Gets the preconditions for a given method."""
        return {v for u, v, label in self.kb.find_edges(source_id=method_id) if label == "has_precondition"}

    def _preconditions_met(self, current_state: set, preconditions: set) -> bool:
        """Checks if all preconditions are met in the current state."""
        return preconditions.issubset(current_state)

    def _get_subtasks(self, method_id: str) -> list:
        """Gets the subtasks for a given method."""
        return [v for u, v, label in self.kb.find_edges(source_id=method_id) if label == "has_subtask"]
