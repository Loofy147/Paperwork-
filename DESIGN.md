# CSAI System Design

This document outlines the architecture and design of the Causal-Symbolic AI (CSAI) system, a neuro-symbolic platform for commonsense reasoning, learning, planning, and collaborative dialogue.

## 1. Core Architecture

The system is a hybrid architecture that combines a symbolic reasoning core with neural modules for learning, perception, and dialogue.

*   **Symbolic Core:**
    *   **Knowledge Base:** A graph-based database for storing and managing commonsense knowledge, including temporal, action-based, and abstract task information.
    *   **Reasoning Engines:** A suite of engines for performing logical, causal, counterfactual, and temporal inference.
    *   **Planning Module:** A hierarchical, goal-oriented planner that can generate and decompose plans.
*   **Neural & State-Based Modules:**
    *   **Perception Module:** Translates natural language queries and commands into a structured, machine-readable format.
    *   **Action Module:** Translates reasoned output and plans back into natural language.
    *   **Knowledge Acquisition Module:** Extracts new knowledge from unstructured text.
    *   **Visual Grounding Module:** Links symbolic concepts to visual data.
    *   **Dialogue Manager:** Manages the state and flow of the conversation.

## 2. Symbolic Core

### 2.1. Knowledge Representation for Hierarchical Planning

To support hierarchical planning, the knowledge base will be evolved to represent abstract tasks and their decompositions.

*   **Abstract Tasks:** High-level tasks (e.g., `achieve_dry_grass`) will be represented as nodes.
*   **Methods:** Actions will now be considered "methods" that can achieve a task. Each abstract task can have multiple methods. Methods are linked to abstract tasks via a `decomposes` edge.
*   **STRIPS-Style Actions:** Primitive actions will continue to be represented using the STRIPS formalism, with `precondition`, `add_effect`, and `delete_effect` edges.

### 2.2. Reasoning and Planning

*   **Hierarchical Planner:** The `Planner` will be upgraded to a Hierarchical Task Network (HTN) planner. Given a high-level goal, it will find abstract tasks that can achieve that goal and then recursively decompose them into sub-tasks until a concrete, executable plan is formed.
*   **Temporal Reasoning Engine:** Will continue to support reasoning about time and sequences.

## 3. Dialogue and Collaboration

### 3.1. Dialogue Manager

A new `DialogueManager` module will be introduced to enable multi-turn, collaborative conversations.

*   **Functionality:** The Dialogue Manager will maintain a `DialogueState`, tracking the current user intent, the conversation history, and any pending questions or choices.
*   **State-Based Approach:** It will use a simple, state-based model. For example, when the planner finds multiple methods to achieve a goal, the Dialogue Manager will enter a "clarification" state and ask the user for input.

## 4. System Integration

The `CSAISystem` will be upgraded to be a conversational agent. The interactive REPL will be updated to handle multi-turn dialogues.

*   **Conversational Flow:** The main loop will now be driven by the `DialogueManager`. The system will be able to ask clarifying questions and understand contextual replies.
*   **Example Interaction:**
    *   User: `plan for dry grass`
    *   AI: `I have two ways to achieve that: wait for the sun, or turn off the sprinkler. The sprinkler is currently on. Which method should I use?`
    *   User: `wait for the sun`
    *   AI: `Here is the plan: 1. wait for sun`
