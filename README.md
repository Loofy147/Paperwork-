# Neuro-Symbolic AI (CSAI) Prototype

This project is a Python-based prototype of a Neuro-Symbolic AI (CSAI) system designed for commonsense reasoning, learning, and visual grounding. It is the practical implementation of the ideas presented in the research paper, "The Missing Fundamentals of AI: A New Approach to Commonsense Reasoning."

## Overview

The CSAI system is a hybrid architecture that combines a symbolic reasoning core with neural modules for learning and perception. It is a departure from purely statistical, large-scale language models, and a step towards a more hybrid approach to AI that can reason about the world in a more structured and causal way, and can also learn from new information and ground its knowledge in the visual world.

The system is composed of the following modules:

*   **Symbolic Core:**
    *   **Knowledge Base:** A graph-based database for storing and managing commonsense knowledge.
    *   **Reasoning Engines:** A suite of engines for performing logical, causal, and counterfactual inference.
*   **Neural Modules:**
    *   **Perception Module:** Translates natural language queries into a structured, machine-readable format.
    *   **Action Module:** Translates reasoned output back into natural language.
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

You can ask different types of questions, including causal and counterfactual questions:

```
> Why is the grass wet?
The wet grass is caused by rain or sprinkler.

> What would happen to the wet grass if it had not rained?
If it had not rained, the wet grass would still have occurred, but it would only be caused by sprinkler.
```

You can also use the new neuro-symbolic capabilities:

```
> learn facts.txt
I have learned new facts from the text.

> ground bird in ./images
I believe the best image for 'bird' is 'sparrow.jpg'.
```

## Key Features

### Neuro-Symbolic Capabilities

The CSAI system bridges the gap between symbolic reasoning and neural learning with two key features:

*   **Knowledge Acquisition:** The system can learn new facts from unstructured text. The `learn` command triggers a `KnowledgeAcquirer` module that uses `spaCy` to parse text and extract new relationships, which are then added to the knowledge base. This breaks the static knowledge bottleneck and allows the AI to learn and adapt.
*   **Visual Symbol Grounding:** The system can ground the abstract symbols in its knowledge base to the perceptual world. The `ground` command uses a `VisualGrounder` module that leverages the pre-trained CLIP model to find the best image for a given concept in a directory of images. This addresses the symbol grounding problem and connects the AI's knowledge to visual reality.

### Advanced Reasoning

*   **Counterfactual Reasoning:** The system can answer "what if" questions by simulating hypothetical scenarios. It creates a temporary copy of its knowledge graph, applies an "intervention" (e.g., removing a cause), and then reasons over this modified reality.
*   **Causal Reasoning:** The system can answer "why" questions by traversing a knowledge graph that contains explicit causal relationships.

### Time-Aware Computing

The CSAI system incorporates **Time-Aware Computing**. All reasoning queries can be executed with a `deadline`, and if the system cannot find a complete answer within the timeframe, it will return the best partial result it has found.

## Running the Tests

The project includes a comprehensive test suite using `pytest`. To run all tests, execute the following command from the root of the project:

```bash
PYTHONPATH=. pytest
```
