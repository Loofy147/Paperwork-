import sys
import os
import re

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from csai.csai import CSAISystem

def main():
    """
    An interactive Read-Eval-Print Loop (REPL) for the CSAISystem.
    """
    csai = CSAISystem()
    print("="*50)
    print(" Welcome to the Causal-Symbolic AI (CSAI) System")
    print("="*50)
    print("You can ask questions, or teach me new things.")
    print("Example commands:")
    print("  - What color is a raven?")
    print("  - deadline=1 What is a lion?")
    print("  - learn facts.txt")
    print("  - ground bird in ./images")
    print("\nType 'exit' to quit.")
    print("-"*50)

    try:
        while True:
            try:
                user_input = input("> ")
                if user_input.lower().strip() == "exit":
                    print("Exiting CSAI system. Goodbye!")
                    break

                # Check for 'learn' command
                learn_match = re.match(r"learn\s+(.*)", user_input, re.IGNORECASE)
                if learn_match:
                    file_path = learn_match.group(1).strip()
                    response = csai.learn(file_path)
                    print(response)
                    continue

                # Check for 'ground' command
                ground_match = re.match(r"ground\s+([\w_]+)\s+in\s+(.*)", user_input, re.IGNORECASE)
                if ground_match:
                    concept = ground_match.group(1).strip()
                    image_dir = ground_match.group(2).strip()
                    response = csai.ground(concept, image_dir)
                    print(response)
                    continue

                # Default to asking a question
                deadline = 1.0 # default deadline
                deadline_match = re.match(r"deadline=(\d+)\s*(.*)", user_input)
                question = user_input
                if deadline_match:
                    deadline = int(deadline_match.group(1)) / 1000.0
                    question = deadline_match.group(2)

                response = csai.ask(question, deadline=deadline)
                print(response)

            except EOFError:
                print("\nExiting CSAI system. Goodbye!")
                break

    except KeyboardInterrupt:
        print("\nExiting CSAI system. Goodbye!")

if __name__ == "__main__":
    main()
