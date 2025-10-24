from enum import Enum, auto

class DialogueState(Enum):
    IDLE = auto()
    AWAITING_CHOICE = auto()

class DialogueManager:
    """
    Manages the state and flow of the conversation.
    """
    def __init__(self):
        """
        Initializes the DialogueManager.
        """
        self.state = DialogueState.IDLE
        self.pending_choices = {}

    def start_clarification(self, choices: dict) -> str:
        """
        Starts a clarification dialogue with the user.

        Args:
            choices (dict): A dictionary of choices for the user.

        Returns:
            str: The clarification question to ask the user.
        """
        self.state = DialogueState.AWAITING_CHOICE
        self.pending_choices = choices

        question = "I have a few options to achieve that. Which one should I use?\n"
        for key, value in choices.items():
            question += f"  - {key}: {value}\n"
        return question

    def handle_user_response(self, response: str) -> str | None:
        """
        Handles the user's response to a clarification question.

        Args:
            response (str): The user's response.

        Returns:
            str or None: The chosen option, or None if the response is invalid.
        """
        if self.state == DialogueState.AWAITING_CHOICE:
            self.state = DialogueState.IDLE
            if response in self.pending_choices:
                return self.pending_choices[response]

        return None
