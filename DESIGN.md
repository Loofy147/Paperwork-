# CSAI System Design

This document outlines the architecture and design of the Causal-Symbolic AI (CSAI) system, a neuro-symbolic platform for commonsense reasoning, learning, and visual grounding.

## 1. Core Architecture

The system is a hybrid architecture that combines a symbolic reasoning core with neural modules for learning and perception.

*   **Symbolic Core:**
    *   **Knowledge Base:** A graph-based database for storing and managing commonsense knowledge.
    *   **Reasoning Engines:** A suite of engines for performing logical, causal, and counterfactual inference.
*   **Neural Modules:**
    *   **Perception Module:** Translates natural language queries into a structured, machine-readable format.
    *   **Action Module:** Translates reasoned output back into natural language.
    *   **Knowledge Acquisition Module:** Extracts new knowledge from unstructured text.
    *   **Visual Grounding Module:** Links symbolic concepts to visual data.

## 2. Symbolic Core

### 2.1. Knowledge Representation

The knowledge base is a directed graph where nodes are concepts and edges are relationships.

*   **Nodes:** Represent objects, concepts, or events.
*   **Edges:** Represent relationships, such as `is_a`, `has_property`, `causes`, and `prevents`.

### 2.2. Reasoning Engines

The system includes a set of specialized engines for different reasoning tasks:

*   **Transitive Reasoning Engine:** Handles taxonomic queries (e.g., "What is a raven?").
*   **Causal Reasoning Engine:** Answers "why" questions by traversing causal chains.
*   **Counterfactual Reasoning Engine:** Answers "what if" questions by simulating interventions on a copy of the knowledge graph.

## 3. Neural Modules

### 3.1. Knowledge Acquisition Module (The "Learner")

To overcome the static knowledge bottleneck, this module will enable the system to learn from text.

*   **Functionality:** Given a plain text file, the module will parse the sentences, identify entities, and extract new relationships to be added to the knowledge base.
*   **Technology:** It will use `spaCy` for dependency parsing and rule-based pattern matching to identify subject-verb-object triples that can be translated into new knowledge graph edges.

### 3.2. Visual Grounding Module (The "Seer")

To address the symbol grounding problem, this module will connect the abstract symbols in the knowledge base to the perceptual world.

*   **Functionality:** Given a symbolic concept and a set of images, the module will identify which images are the best visual representation of that concept.
*   **Technology:** It will use the pre-trained **CLIP (Contrastive Language-Image Pre-Training)** model. The module will encode the textual label of the concept and the images into a shared embedding space and then calculate the cosine similarity to find the best match. This allows for powerful, zero-shot visual identification.

## 4. System Integration

The `CSAISystem` will be updated to orchestrate the new learning and grounding modules. The interactive REPL will be extended with new commands:

*   `learn <filename>`: Triggers the Knowledge Acquisition Module to read a text file and update the knowledge base.
*   `ground <concept> in <image_directory>`: Triggers the Visual Grounding Module to find the best image for a given concept in a directory of images.

All reasoning engines will continue to support **Time-Aware Computing**, allowing for queries to be executed under a deadline.
