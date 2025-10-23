# Neuro-Symbolic AI (CSAI) Prototype

This project is a Python-based prototype of a Neuro-Symbolic AI (CSAI) system designed for commonsense reasoning, learning, planning, and visual grounding. It is the practical implementation of the ideas presented in the research paper, "The Missing Fundamentals of AI: A New Approach to Commonsense Reasoning."

## Overview

The CSAI system is a hybrid architecture that combines a symbolic reasoning core with neural modules for learning and perception. It is a departure from purely statistical, large-scale language models, and a step towards a more hybrid approach to AI that can reason about the world, learn from new information, ground its knowledge in the visual world, and generate plans to achieve goals.

The system is composed of the following modules:

*   **Symbolic Core:**
    *   **Knowledge Base:** A graph-based database for storing and managing commonsense knowledge, including temporal and action-based information.
    *   **Reasoning Engines:** A suite of engines for performing logical, causal, counterfactual, and temporal inference.
    *   **Planning Module:** A goal-oriented planner that can generate a sequence of actions to achieve a desired state.
*   **Neural Modules:**
    *   **Perception Module:** Translates natural language queries and commands into a structured, machine-readable format.
    *   **Action Module:** Translates reasoned output and plans back into natural language.
    *   **Knowledge Acquisition Module:** Extracts new knowledge from unstructured text.
    *   **Visual Grounding Module:** Links symbolic concepts to visual data.

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

The CSAI system is best experienced through its interactive REPL.

### Interactive Mode (REPL)

To launch the REPL, run the `main.py` script.

```bash
PYTHONPATH=. python3 main.py
```

You can then type your questions at the prompt. To exit, type `exit`.

You can ask different types of questions, use the neuro-symbolic capabilities, or ask the system to generate a plan:

```
> Why is the grass wet?
The wet grass is caused by rain or sprinkler.

> What would happen to the wet grass if it had not rained?
If it had not rained, the wet grass would still have occurred, but it would only be caused by sprinkler.

> learn facts.txt
I have learned new facts from the text.

> ground bird in ./images
I believe the best image for 'bird' is 'sparrow.jpg'.

> plan for dry_grass
Here is the plan:
1. wait for sun
```

## Key Features

### Goal-Oriented Planning

The system is no longer just a passive oracle; it is a proactive agent that can generate plans to achieve goals. The `plan for` command triggers a `Planner` module that uses a backward-chaining search to find a sequence of actions that will transform the current state of the world into a desired goal state. This is a major step towards autonomous agency.

### Neuro-Symbolic Capabilities

The CSAI system bridges the gap between symbolic reasoning and neural learning with two key features:

*   **Knowledge Acquisition:** The system can learn new facts from unstructured text.
*   **Visual Symbol Grounding:** The system can ground the abstract symbols in its knowledge base to the perceptual world.

### Advanced Reasoning

*   **Temporal Reasoning:** The system can reason about time and sequences, answering questions like "What happened after the rain?".
*   **Counterfactual Reasoning:** The system can answer "what if" questions by simulating hypothetical scenarios.
*   **Causal Reasoning:** The system can answer "why" questions by traversing a knowledge graph that contains explicit causal relationships.

### Time-Aware Computing

All reasoning and planning queries can be executed with a `deadline`, and if the system cannot find a complete answer within the timeframe, it will return the best partial result it has found.

## Running the Tests

The project includes a comprehensive test suite using `pytest`. To run all tests, execute the following command from the root of the project:

```bash
PYTHONPATH=. pytest
```
