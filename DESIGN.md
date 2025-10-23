# CSAI System Design

This document outlines the architecture and design of the Causal-Symbolic AI (CSAI) system, a neuro-symbolic platform for commonsense reasoning, learning, planning, and visual grounding.

## 1. Core Architecture

The system is a hybrid architecture that combines a symbolic reasoning core with neural modules for learning and perception.

*   **Symbolic Core:**
    *   **Knowledge Base:** A graph-based database for storing and managing commonsense knowledge, including temporal and action-based information.
    *   **Reasoning Engines:** A suite of engines for performing logical, causal, counterfactual, and temporal inference.
    *   **Planning Module:** A goal-oriented planner that can generate a sequence of actions to achieve a desired state.
*   **Neural Modules:**
    *   **Perception Module:** Translates natural language queries and commands into a structured, machine-readable format.
    *   **Action Module:** Translates reasoned output and plans back into natural language.
    *   **Knowledge Acquisition Module:** Extracts new knowledge from unstructured text.
    *   **Visual Grounding Module:** Links symbolic concepts to visual data.

## 2. Symbolic Core

### 2.1. Knowledge Representation for Planning

To support planning, the knowledge base will be evolved to represent states, actions, and time.

*   **State Representation:** Facts will no longer be static. They will be represented as nodes with temporal properties, allowing the system to reason about the state of the world at different points in time.
*   **Action Representation:** Actions will be represented as nodes in the graph. Inspired by the STRIPS formalism, actions will be connected to other nodes via new edge types:
    *   `has_precondition`: A condition that must be true for the action to be performed.
    *   `has_add_effect`: A state that becomes true after the action is performed.
    *   `has_delete_effect`: A state that becomes false after the action is performed.

### 2.2. Reasoning and Planning

*   **Temporal Reasoning Engine:** A new engine responsible for answering questions about time and sequences (e.g., "What happened after the rain?"). This is a crucial prerequisite for planning.
*   **Planning Module:** The core of the new agency. Given a goal state, the planner will use a search algorithm (e.g., backward-chaining) to find a sequence of actions that can transform the current state of the world into the desired goal state.

### 2.3. Existing Reasoning Engines

The system will continue to support its existing reasoning capabilities:

*   **Transitive Reasoning Engine:** For taxonomic queries.
*   **Causal Reasoning Engine:** For "why" questions.
*   **Counterfactual Reasoning Engine:** For "what if" questions.

## 3. Neural Modules

The existing neural modules will be updated to support the new planning capabilities.

*   **Perception Module:** Will be taught to understand goal-oriented commands (e.g., `plan for <goal>`).
*   **Action Module:** Will be updated to present the generated plans in a clear, step-by-step format.
*   **Knowledge Acquisition Module:** Can be extended in the future to learn new actions from text.
*   **Visual Grounding Module:** Can be used to ground the preconditions and effects of actions in the visual world.

## 4. System Integration

The `CSAISystem` will be upgraded to orchestrate the new planning capabilities. The interactive REPL will be extended with a new, powerful command:

*   `plan for <goal>`: Triggers the Planning Module to generate a sequence of actions to achieve the specified goal.
