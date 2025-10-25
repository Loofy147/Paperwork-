import sys
import os
import re

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from csai.csai import CSAISystem
from csai.dialogue.dialogue_manager import DialogueState

def main():
    """An interactive Read-Eval-Print Loop (REPL) for the CSAISystem.

    This function provides a command-line interface for interacting with the
    CSAI system. It allows users to ask questions and receive answers in a
    conversational manner. The REPL continues until the user types 'exit' or
    presses Ctrl+C.
    """
    csai = CSAISystem()
    print("="*50)
    print(" Welcome to the Causal-Symbolic AI (CSAI) System")
    print("="*50)
    print("You can ask questions, teach me new things, or ask me to plan.")
    print("Example commands:")
    print("  - What color is a raven?")
    print("  - learn facts.txt")
    print("  - ground bird in ./images")
    print("  - plan for dry_grass")
    print("\nType 'exit' to quit.")
    print("-"*50)

    try:
        while True:
            try:
                user_input = input("> ").strip()
                if user_input.lower() == "exit":
                    print("Exiting CSAI system. Goodbye!")
                    break

                # If the system is awaiting a choice, handle the response.
                if csai.dialogue_manager.state == DialogueState.AWAITING_CHOICE:
                    chosen_method_key = user_input
                    goal = csai.dialogue_manager.pending_choices.get("goal")
                    chosen_method_id = csai.dialogue_manager.pending_choices.get(chosen_method_key)

                    if chosen_method_id and goal:
                        response = csai.plan(goal=goal, chosen_method=chosen_method_id)
                        print(response)
                    else:
                        print("Invalid choice. Please try again.")
                    csai.dialogue_manager.state = DialogueState.IDLE
                    continue

                # Check for 'learn' command
                learn_match = re.match(r"learn\s+(.*)", user_input, re.IGNORECASE)
                if learn_match:
                    file_path = learn_match.group(1)
                    response = csai.learn(file_path)
                    print(response)
                    continue

                # Check for 'ground' command
                ground_match = re.match(r"ground\s+([\w_]+)\s+in\s+(.*)", user_input, re.IGNORECASE)
                if ground_match:
                    concept, image_dir = ground_match.groups()
                    response = csai.ground(concept, image_dir)
                    print(response)
                    continue

                # Check for 'plan' command
                plan_match = re.match(r"plan for\s+(.*)", user_input, re.IGNORECASE)
                if plan_match:
                    goal = plan_match.group(1).replace(" ", "_")
                    response = csai.plan(goal)
                    if isinstance(response, str) and "Which one should I use?" in response:
                        csai.dialogue_manager.pending_choices["goal"] = goal
                    print(response)
                    continue

                # Default to asking a question
                response = csai.ask(user_input)
                print(response)

            except EOFError:
                print("\nExiting CSAI system. Goodbye!")
                break

    except KeyboardInterrupt:
        print("\nExiting CSAI system. Goodbye!")

if __name__ == "__main__":
    main()
