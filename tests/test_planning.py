import pytest
from csai.csai import CSAISystem

@pytest.fixture
def csai_system():
    """Provides a fully populated CSAISystem for integration tests."""
    system = CSAISystem()
    return system

def test_temporal_reasoning(csai_system):
    """
    Tests the AI's ability to reason about temporal sequences.
    """
    response = csai_system.ask("What happened after the rain?")
    assert "After the rain, the following events occurred: sprinkler" in response

def test_planning(csai_system):
    """
    Tests the AI's ability to generate a plan to achieve a goal.
    """
    response = csai_system.plan("dry_grass")
    assert "Here is the plan:" in response
    assert "1. wait for sun" in response
