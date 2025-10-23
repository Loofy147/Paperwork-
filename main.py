import sys
import os

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
    print("Example questions:")
    print("  - What color is a raven?")
    print("  - What is a lion?")
    print("  - Does a bird have wings?")
    print("  - What type of animal is a tiger?")
    print("\nType 'exit' to quit.")
    print("-"*50)

    try:
        while True:
            try:
                question = input("> ")
                if question.lower().strip() == "exit":
                    print("Exiting CSAI system. Goodbye!")
                    break

                response = csai.ask(question)
                print(response)
            except EOFError:
                print("\nExiting CSAI system. Goodbye!")
                break

    except KeyboardInterrupt:
        print("\nExiting CSAI system. Goodbye!")

if __name__ == "__main__":
    main()
