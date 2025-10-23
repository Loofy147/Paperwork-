import pytest
import os
from csai.csai import CSAISystem

@pytest.fixture
def csai_system():
    """Provides a fully populated CSAISystem for integration tests."""
    system = CSAISystem()
    return system

def test_knowledge_acquisition(csai_system):
    """
    Tests the AI's ability to learn new facts from a text file.
    """
    # Create a dummy text file with new facts
    facts_text = "A sparrow is a bird. A sparrow has wings."
    with open("test_facts.txt", "w") as f:
        f.write(facts_text)

    # Learn from the file
    response = csai_system.learn("test_facts.txt")
    assert "I have learned new facts from the text." in response

    # Verify that the new knowledge is in the knowledge base
    response = csai_system.ask("What is a sparrow?")
    assert "A sparrow is a type of" in response
    assert "bird" in response

    # Clean up the dummy file
    os.remove("test_facts.txt")

def test_visual_grounding(csai_system):
    """
    Tests the AI's ability to ground a concept in an image.
    """
    # Create a dummy image directory and a dummy image
    os.makedirs("test_images", exist_ok=True)
    from PIL import Image
    dummy_image = Image.new('RGB', (100, 100), color = 'red')
    dummy_image.save("test_images/red_square.png")

    # Create another dummy image
    dummy_image_blue = Image.new('RGB', (100, 100), color = 'blue')
    dummy_image_blue.save("test_images/blue_square.png")

    # Ground the concept 'red'
    response = csai_system.ground("red", "test_images")
    assert "I believe the best image for 'red' is 'red_square.png'." in response

    # Clean up the dummy directory and image
    os.remove("test_images/red_square.png")
    os.remove("test_images/blue_square.png")
    os.rmdir("test_images")
