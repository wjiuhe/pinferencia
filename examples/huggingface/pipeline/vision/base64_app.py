import base64
from io import BytesIO

from PIL import Image
from transformers import pipeline

from pinferencia import Server

vision_classifier = pipeline(task="image-classification")


def classify(images: list) -> list:
    """Image Classification

    Args:
        images (list): list of base64 encoded image strings

    Returns:
        list: list of classification results
    """
    input_images = [Image.open(BytesIO(base64.b64decode(img))) for img in images]
    return vision_classifier(images=input_images)


service = Server()
service.register(model_name="vision", model=classify)
