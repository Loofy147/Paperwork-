import os
from transformers import CLIPProcessor, CLIPModel
from PIL import Image

class VisualGrounder:
    """
    Grounds symbolic concepts in the knowledge base to visual data using CLIP.
    """

    def __init__(self):
        """
        Initializes the VisualGrounder and loads the pre-trained CLIP model.
        """
        self.model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
        self.processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

    def ground_concept(self, concept_name: str, image_directory: str) -> str | None:
        """
        Finds the best image in a directory to represent a given concept.

        Args:
            concept_name (str): The name of the concept to ground (e.g., 'bird').
            image_directory (str): The path to the directory of images to search.

        Returns:
            str or None: The filename of the best matching image, or None if no suitable
                         image is found.
        """
        if not os.path.isdir(image_directory):
            return None

        image_paths = [os.path.join(image_directory, f) for f in os.listdir(image_directory)
                       if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

        if not image_paths:
            return None

        # Prepare the text and image inputs for CLIP
        texts = [f"a photo of a {concept_name.replace('_', ' ')}"]
        images = [Image.open(path) for path in image_paths]

        inputs = self.processor(text=texts, images=images, return_tensors="pt", padding=True)
        outputs = self.model(**inputs)

        # Calculate the similarity between the text and each image
        logits_per_image = outputs.logits_per_image
        probs = logits_per_image.softmax(dim=1)

        # Find the image with the highest probability
        best_image_index = probs.argmax().item()

        return os.path.basename(image_paths[best_image_index])
