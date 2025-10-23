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
    print("You can ask questions about the knowledge base.")
    print("You can also specify a deadline in milliseconds (e.g., deadline=500).")
    print("Example questions:")
    print("  - What color is a raven?")
    print("  - deadline=1 What is a lion?")
    print("  - Does a bird have wings?")
    print("\nType 'exit' to quit.")
    print("-"*50)

    try:
        while True:
            try:
                question = input("> ")
                if question.lower().strip() == "exit":
                    print("Exiting CSAI system. Goodbye!")
                    break

                deadline = 1.0 # default deadline
                match = re.match(r"deadline=(\d+)\s*(.*)", question)
                if match:
                    deadline = int(match.group(1)) / 1000.0
                    question = match.group(2)

                response = csai.ask(question, deadline=deadline)
                print(response)
            except EOFError:
                print("\nExiting CSAI system. Goodbye!")
                break

    except KeyboardInterrupt:
        print("\nExiting CSAI system. Goodbye!")

if __name__ == "__main__":
    main()
