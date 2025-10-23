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

def test_has_part_positive(csai_system):
    response = csai_system.ask("Does a raven have wings?")
    assert response == "Yes, a raven has wings."

def test_has_part_negative(csai_system):
    response = csai_system.ask("Does a cat have wings?")
    assert response == "No, a cat does not have wings."

def test_new_animal_property(csai_system):
    response = csai_system.ask("What color is a tiger?")
    assert response == "A tiger is orange."

def test_new_animal_is_a(csai_system):
    response = csai_system.ask("What is a lion?")
    assert "A lion is a type of" in response
    assert "animal" in response
    assert "cat" in response
    assert "living_thing" in response
    assert "mammal" in response

def test_deadline_tight(csai_system):
    response = csai_system.ask("What is a lion?", deadline=0.000001)
    # With a tight deadline, we expect either a partial result or a timeout message.
    assert response != "A lion is a type of animal, cat, living_thing, mammal."

    is_partial_result = "A lion is a type of" in response
    is_timeout_message = "deadline was too short" in response

    assert is_partial_result or is_timeout_message, f"Unexpected response: {response}"

def test_deadline_generous(csai_system):
    response = csai_system.ask("What is a lion?", deadline=1.0)
    # With a generous deadline, we expect a full result
    assert "A lion is a type of" in response
    assert "animal" in response
    assert "cat" in response
    assert "living_thing" in response
    assert "mammal" in response
