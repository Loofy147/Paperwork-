from csai.knowledge_base.knowledge_base import KnowledgeBase

class Planner:
    """
    A simple goal-oriented planner that uses a backward-chaining search to find a
    sequence of actions to achieve a goal.
    """

    def __init__(self, knowledge_base: KnowledgeBase):
        """
        Initializes the Planner.

        Args:
            knowledge_base (KnowledgeBase): The knowledge base to use for planning.
        """
        self.kb = knowledge_base

    def find_plan(self, current_state: set, goal_state: set) -> list | None:
        """
        Finds a sequence of actions to achieve a goal state from a current state.

        Args:
            current_state (set): A set of propositions representing the current state.
            goal_state (set): A set of propositions representing the goal state.

        Returns:
            list or None: A list of action IDs representing the plan, or None if no
                          plan is found.
        """
        # If the goal is already met, the plan is empty.
        if goal_state.issubset(current_state):
            return []

        # Find all actions in the knowledge base.
        actions = [
            node_id for node_id, props in self.kb.graph.nodes(data=True)
            if props.get("type") == "action"
        ]

        # Try to find a plan by recursively searching backward from the goal.
        return self._search(current_state, goal_state, actions, [])

    def _search(self, current_state: set, goal_state: set, actions: list, plan: list) -> list | None:
        """
        The recursive search function for the planner.
        """
        # Find a goal that is not yet satisfied.
        unmet_goal = next((g for g in goal_state if g not in current_state), None)
        if unmet_goal is None:
            return plan # All goals are met

        # Find actions that can achieve the unmet goal.
        possible_actions = [
            action_id for action_id in actions
            if (action_id, unmet_goal, "has_add_effect") in self.kb.graph.edges(data="label")
        ]

        for action in possible_actions:
            preconditions = {
                u for u, _, label in self.kb.find_edges(source_id=action)
                if label == "has_precondition"
            }

            # Recursively plan to meet the preconditions.
            sub_plan = self._search(current_state, preconditions, actions, plan)
            if sub_plan is not None:
                new_state = self._apply_action(current_state, action)
                final_plan = self._search(new_state, goal_state, actions, sub_plan + [action])
                if final_plan is not None:
                    return final_plan

        return None # No plan found

    def _apply_action(self, state: set, action_id: str) -> set:
        """
        Applies an action to a state to produce a new state.
        """
        new_state = set(state)

        add_effects = {
            v for _, v, label in self.kb.find_edges(source_id=action_id)
            if label == "has_add_effect"
        }
        delete_effects = {
            v for _, v, label in self.kb.find_edges(source_id=action_id)
            if label == "has_delete_effect"
        }

        new_state.difference_update(delete_effects)
        new_state.update(add_effects)

        return new_state
