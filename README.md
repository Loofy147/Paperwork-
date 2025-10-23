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

You can ask different types of questions, including causal and counterfactual questions:

```
> Why is the grass wet?
The wet grass is caused by rain or sprinkler.

> What would happen to the wet grass if it had not rained?
If it had not rained, the wet grass would still have occurred, but it would only be caused by sprinkler.
```

You can also specify a timeout for the reasoning process using the `--deadline` flag. For example:

```
> What is a raven? --deadline=0.001
```

If the deadline is too short, the system may return a partial result or a message indicating that it timed out. The default deadline is 1.0 second.

## Key Features

### Counterfactual Reasoning

Fulfilling a major gap in the AI industry, the CSAI system can perform **counterfactual reasoning**. It can answer "what if" questions by simulating hypothetical scenarios. The system achieves this by creating a temporary copy of its knowledge graph, applying an "intervention" (e.g., removing a cause), and then reasoning over this modified reality to determine the new outcome. This allows for a deeper, more robust form of explainability and decision analysis.

### Causal Reasoning

The system is capable of performing basic causal reasoning to answer "why" questions. It does this by traversing a knowledge graph that contains explicit causal relationships (e.g., "rain" -> "causes" -> "wet grass"). When asked a question like "Why is the grass wet?", the system searches for nodes that have a `causes` relationship with the "wet grass" node and returns them as an explanation.

### Time-Aware Computing

The CSAI system incorporates **Time-Aware Computing**, one of the missing computational fundamentals discussed in the research paper. This feature allows the system to perform reasoning under time constraints.

When a query is executed, a `deadline` can be specified. If the system cannot find a complete answer within the given timeframe, it will return the best partial result it has found so far, or a message indicating that the deadline was too short to produce a meaningful result. This makes the system more robust and suitable for real-world applications where response time is critical.

## Running the Tests

The project includes a comprehensive test suite using `pytest`. To run the tests, execute the following command from the root of the project:

```bash
PYTHONPATH=. pytest tests/test_csai.py
```

This will discover and run all the tests in the `tests` directory and report the results.
