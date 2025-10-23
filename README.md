# Causal-Symbolic AI (CSAI) Prototype

This project is a Python-based prototype of a Causal-Symbolic AI (CSAI) system designed for commonsense reasoning. It is the practical implementation of the ideas presented in the research paper, "The Missing Fundamentals of AI: A New Approach to Commonsense Reasoning."

## Overview

The CSAI system is designed to answer commonsense questions by combining a structured knowledge base with a logical inference engine. It is a departure from purely statistical, large-scale language models, and a step towards a more hybrid approach to AI that can reason about the world in a more structured and causal way.

The system is composed of four main modules:

*   **Knowledge Base:** A graph-based database for storing commonsense knowledge.
*   **Perception Module:** Translates natural language queries into a structured, machine-readable format.
*   **Reasoning Engine:** Performs logical inference on the structured query.
*   **Action Module:** Translates the reasoned output back into a natural language response.

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

The CSAI system can be run in two modes: as a single-execution script, or as an interactive REPL.

### Single Execution

To ask a single question, you can run the `csai/csai.py` file directly.

```bash
PYTHONPATH=. python3 csai/csai.py
```

This will execute the default question in the `__main__` block and print the answer.

### Interactive Mode (REPL)

For a more interactive experience, you can run the `main.py` script. This will launch a Read-Eval-Print Loop (REPL) that allows you to ask multiple questions in a session.

```bash
PYTHONPATH=. python3 main.py
```

You can then type your questions at the prompt. To exit, type `exit`.

## Running the Tests

The project includes a comprehensive test suite using `pytest`. To run the tests, execute the following command from the root of the project:

```bash
PYTHONPATH=. pytest tests/test_csai.py
```

This will discover and run all the tests in the `tests` directory and report the results.
