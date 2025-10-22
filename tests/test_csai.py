import pytest
from csai.csai import CSAISystem

@pytest.fixture
def csai_system():
    """Provides a fully populated CSAISystem for integration tests."""
    system = CSAISystem()
    return system

def test_property_query(csai_system):
    response = csai_system.ask("What color is a canary?")
    assert response == "A canary is yellow."

def test_is_a_query_simple(csai_system):
    response = csai_system.ask("What is a crow?")
    # The order of the inferred types is not guaranteed, so we check for all expected parts.
    assert "A crow is a type of" in response
    assert "animal" in response
    assert "bird" in response
    assert "living_thing" in response

def test_transitivity(csai_system):
    response = csai_system.ask("What type of living_thing is a raven?")
    assert response == "A raven is a type of living_thing."

def test_unknown_question(csai_system):
    response = csai_system.ask("This is not a valid question.")
    assert "I don't understand" in response

def test_no_answer(csai_system):
    response = csai_system.ask("What color is a tree?")
    assert "I'm sorry" in response
