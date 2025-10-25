import pytest
from csai.csai import CSAISystem

@pytest.fixture
def csai_system():
    """Provides a CSAISystem for integration tests."""
    system = CSAISystem()
    return system

def test_hierarchical_planning_clarification(csai_system):
    """
    Tests the planner's ability to ask for clarification when multiple
    methods are available.
    """
    csai_system.current_state = {"sprinkler_on", "wet_grass"}
    response = csai_system.plan("dry_grass")
    assert "I have a few options" in response
    assert "method_wait_for_sun" in response
    assert "method_turn_off_sprinkler" in response

def test_dialogue_and_planning(csai_system):
    """
    Tests the full dialogue and planning flow.
    """
    csai_system.current_state = {"sprinkler_on", "wet_grass"}

    # Initial planning request
    response = csai_system.plan("dry_grass")
    assert "I have a few options" in response

    # User chooses a method
    response = csai_system.plan(goal="dry_grass", chosen_method="method_turn_off_sprinkler")
    assert "Here is the plan:" in response
    assert "1. turn off sprinkler" in response

def test_hierarchical_planning_auto_selection(csai_system):
    """
    Tests the HTN planner's ability to auto-select a single valid method.
    """
    csai_system.current_state = {"sprinkler_off", "wet_grass"}
    response = csai_system.plan("dry_grass")
    assert "Here is the plan:" in response
    assert "1. wait for sun" in response

def test_dialogue_invalid_choice(csai_system):
    """
    Tests how the system handles an invalid user choice.
    """
    csai_system.current_state = {"sprinkler_on", "wet_grass"}

    # Initial planning request
    response = csai_system.plan("dry_grass")
    assert "I have a few options" in response

    # User makes an invalid choice
    response = csai_system.plan(goal="dry_grass", chosen_method="invalid_method")
    assert "Invalid choice" in response
