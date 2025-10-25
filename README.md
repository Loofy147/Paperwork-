# Causal-Symbolic AI (CSAI) Prototype

This project is a Python-based prototype of a Causal-Symbolic AI (CSAI) system designed for commonsense reasoning. It is the practical implementation of the ideas presented in the research paper, "The Missing Fundamentals of AI: A New Approach to Commonsense Reasoning."

## Overview

The CSAI system is designed to answer commonsense questions by combining a structured knowledge base with a logical inference engine. It is a departure from purely statistical, large-scale language models, and a step towards a more hybrid approach to AI that can reason about the world in a more structured and causal way.

## Project Structure

The system is composed of four main modules, each in its own subdirectory under `csai/`:

*   **`knowledge_base`:** A graph-based database for storing commonsense knowledge. The `KnowledgeBase` class provides an interface for adding and querying nodes and edges in the graph.
*   **`perception`:** Translates natural language queries into a structured, machine-readable format. The `PerceptionModule` uses regular expressions and `spacy` for lemmatization to parse user input.
*   **`reasoning`:** Performs logical inference on the structured query. The `ReasoningEngine` traverses the knowledge graph to find answers to the user's questions.
*   **`action`:** Translates the reasoned output back into a natural language response. The `ActionModule` generates human-readable sentences from the structured results.

## Setup and Installation

### 1. Create a Virtual Environment

It is recommended to run this project in a virtual environment.

```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies

Install the required packages from the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

This will install `networkx`, `spacy`, `pytest`, and the `en_core_web_sm` model for spacy.

## Running the System

To run the CSAI system, execute the `main.py` script from the root of the project.

```bash
python3 main.py
```

This will launch a Read-Eval-Print Loop (REPL) that allows you to ask multiple questions in a session. You can then type your questions at the prompt. To exit, type `exit`.

## Running the Tests

The project includes a comprehensive test suite using `pytest`. To run the tests, execute the following command from the root of the project:

```bash
PYTHONPATH=. pytest tests/
```

This will discover and run all the tests in the `tests` directory and report the results.

## Contributing

Contributions are welcome! If you would like to contribute to the project, please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contact

For questions or feedback, please contact the development team at [developers@csai.com](mailto:developers@csai.com).
