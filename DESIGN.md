# CSAI System Design

This document outlines the architecture and design of the Causal-Symbolic AI (CSAI) system.

## 1. Core Modules

The system is composed of four main modules:

*   **Knowledge Base:** A graph-based database for storing commonsense knowledge.
*   **Perception Module:** Translates natural language queries into a structured, machine-readable format.
*   **Reasoning Engine:** Performs logical inference on the structured query.
*   **Action Module:** Translates the reasoned output back into a natural language response.

## 2. Knowledge Representation

The knowledge base is a directed graph where nodes represent concepts or entities, and edges represent relationships between them.

*   **Nodes:** Represent objects, concepts, or events (e.g., "raven," "bird," "rain").
*   **Edges:** Represent relationships, such as:
    *   `is_a`: For taxonomic relationships (e.g., "raven" -> "bird").
    *   `has_property`: For attributes (e.g., "raven" -> "black").
    *   `has_part`: For composition (e.g., "bird" -> "wing").
    *   `causes`: For direct causal links (e.g., "rain" -> "wet grass").
    *   `prevents`: For preventative causal links (e.g., "umbrella" -> "getting wet").

## 3. Reasoning

The system's reasoning capabilities are handled by a set of specialized engines.

### 3.1. Transitive Reasoning Engine

This engine is responsible for handling queries that involve transitive relationships, such as "is_a." It uses a breadth-first search to traverse the knowledge graph and infer relationships.

### 3.2. Causal Reasoning Engine

To handle "why" questions, a new **Causal Reasoning Engine** will be introduced. This engine will be responsible for finding and returning causal chains from the knowledge graph.

*   **Functionality:** Given a query like "Why is the grass wet?", the engine will search for incoming `causes` edges to the "wet grass" node. It will then traverse the graph backwards to construct a causal chain (e.g., "The grass is wet because it rained.").
*   **Algorithm:** The engine will use a backward-chaining search algorithm, starting from the effect and looking for its causes.

## 4. Module Updates for Causal Reasoning

The introduction of causal reasoning will require updates to the following modules:

*   **Perception Module:** The query parser will be extended to recognize "why" questions and generate a new type of structured query (e.g., `{"type": "causal_explanation", "event": "wet grass"}`).
*   **Action Module:** The response generator will be updated to format the output of the Causal Reasoning Engine into a human-readable explanation.
*   **CSAISystem:** The main system will be updated to route causal queries to the new `CausalReasoningEngine`.

## 5. Time-Aware Computing

The system incorporates time-aware computing by allowing a `deadline` to be set for each query. If the reasoning process exceeds this deadline, the system returns the best partial result it has found so far. This is handled by the `ReasoningEngine`, which periodically checks the elapsed time during its execution. The new `CausalReasoningEngine` will also incorporate this feature.
