# Neuro-Symbolic AI (CSAI) Prototype

This project is a Python-based prototype of a Neuro-Symbolic AI (CSAI) system designed for commonsense reasoning, learning, planning, and visual grounding. It is the practical implementation of the ideas presented in the research paper, "The Missing Fundamentals of AI: A New Approach to Commonsense Reasoning."

## Overview

The CSAI system is a hybrid architecture that combines a symbolic reasoning core with neural modules for learning and perception. It is a departure from purely statistical, large-scale language models, and a step towards a more hybrid approach to AI that can reason about the world, learn from new information, ground its knowledge in the visual world, and generate plans to achieve goals.

## Project Structure

The system is composed of four main modules, each in its own subdirectory under `csai/`:

*   **`knowledge_base`:** A graph-based database for storing commonsense knowledge. The `KnowledgeBase` class provides an interface for adding and querying nodes and edges in the graph.
*   **`perception`:** Translates natural language queries into a structured, machine-readable format. The `PerceptionModule` uses regular expressions and `spacy` for lemmatization to parse user input.
*   **`reasoning`:** Performs logical inference on the structured query. The `ReasoningEngine` traverses the knowledge graph to find answers to the user's questions.
*   **`action`:** Translates the reasoned output back into a natural language response. The `ActionModule` generates human-readable sentences from the structured results.
The system is composed of the following modules:

*   **Symbolic Core:**
    *   **Knowledge Base:** A graph-based database for storing and managing commonsense knowledge, including temporal and action-based information.
    *   **Reasoning Engines:** A suite of engines for performing logical, causal, counterfactual, and temporal inference.
    *   **Planning Module:** A hierarchical, goal-oriented planner that can generate and decompose plans.
*   **Neural & State-Based Modules:**
    *   **Perception Module:** Translates natural language queries and commands into a structured, machine-readable format.
    *   **Action Module:** Translates reasoned output and plans back into natural language.
    *   **Knowledge Acquisition Module:** Extracts new knowledge from unstructured text.
    *   **Visual Grounding Module:** Links symbolic concepts to visual data.
    *   **Dialogue Manager:** Manages the state and flow of the conversation.

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

This will install `networkx`, `spacy`, `pytest`, `transformers`, `torch`, `Pillow`, and the `en_core_web_sm` model for spacy.

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
The CSAI system is best experienced through its interactive REPL.

### Interactive Mode (REPL)

To launch the REPL, run the `main.py` script.

```bash
PYTHONPATH=. python3 main.py
```

You can then type your questions at the prompt. To exit, type `exit`.

You can ask different types of questions, use the neuro-symbolic capabilities, or engage in a collaborative planning session:

```
> plan for dry_grass
I have a few options to achieve that. Which one should I use?
  - method_wait_for_sun: wait for sun
  - method_turn_off_sprinkler: turn off sprinkler

> method_turn_off_sprinkler
Here is the plan:
1. turn off sprinkler
```

## Key Features

### Collaborative Hierarchical Planning

The system is no longer just a passive planner; it is a collaborative agent that can engage in a dialogue to refine a plan. It uses a Hierarchical Task Network (HTN) planner to reason about abstract goals and decompose them into concrete steps. If it finds multiple valid ways to achieve a goal, it will ask for clarification, allowing the user to guide the planning process.

### Neuro-Symbolic Capabilities

The CSAI system bridges the gap between symbolic reasoning and neural learning with two key features:

*   **Knowledge Acquisition:** The system can learn new facts from unstructured text.
*   **Visual Symbol Grounding:** The system can ground the abstract symbols in its knowledge base to the perceptual world.

### Advanced Reasoning

*   **Temporal Reasoning:** The system can reason about time and sequences.
*   **Counterfactual Reasoning:** The system can answer "what if" questions.
*   **Causal Reasoning:** The system can answer "why" questions.

### Time-Aware Computing

All reasoning and planning queries can be executed with a `deadline`.

## Contributing

Contributions are welcome! If you would like to contribute to the project, please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contact

For questions or feedback, please contact the development team at [developers@csai.com](mailto:developers@csai.com).
The project includes a comprehensive test suite using `pytest`. To run all tests, execute the following command from the root of the project:

```bash
PYTHONPATH=. pytest
```
