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

This engine handles "why" questions by finding and returning causal chains from the knowledge graph. It uses a backward-chaining search to find the causes of a given event.

### 3.3. Counterfactual Reasoning Engine

To answer "what if" questions, a **Counterfactual Reasoning Engine** will be introduced. This engine will simulate hypothetical scenarios by performing "interventions" on the knowledge graph.

*   **Functionality:** Given a query like "What if it had not rained?", the engine will determine the likely outcome.
*   **Algorithm:**
    1.  **Copy:** Create a temporary, in-memory copy of the knowledge graph to avoid altering the base knowledge.
    2.  **Intervene:** Apply an "intervention" to the copied graph. This involves removing the specified event and its direct causal effects. For example, for the query "What if it had not rained?", the "rain" node and its outgoing `causes` edges would be removed.
    3.  **Re-evaluate:** Use the existing `CausalReasoningEngine` to reason over the modified graph and determine the new state of the world. For example, it would re-evaluate the state of "wet grass."
    4.  **Compare:** The engine will compare the outcome from the modified graph with the outcome from the original graph to generate a comparative answer.

## 4. Module Updates for Counterfactual Reasoning

The introduction of counterfactual reasoning will require updates to the following modules:

*   **Perception Module:** The query parser will be extended to recognize "what if" questions and generate a new `counterfactual` query type (e.g., `{"type": "counterfactual", "intervention": "remove", "event": "rain"}`).
*   **Action Module:** The response generator will be updated to format the output of the Counterfactual Reasoning Engine into a clear, comparative statement (e.g., "If it had not rained, the grass would be dry.").
*   **CSAISystem:** The main system will be updated to route counterfactual queries to the new `CounterfactualReasoningEngine`.

## 5. Time-Aware Computing

All reasoning engines, including the new `CounterfactualReasoningEngine`, will incorporate time-aware computing. They will adhere to the `deadline` parameter and return partial results if the reasoning process is interrupted.
