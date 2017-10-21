import io
import os

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

# img_name is the name of the image file (e.g. RedApple.jpg)
def what_object(img_name):

    # Instantiates a client
    client = vision.ImageAnnotatorClient()

    # The name of the image file to annotate
    file_name = os.path.join(
        os.path.dirname(__file__),
        ('resources/' + img_name))

    # Loads the image into memory
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    # Performs label detection on the image file
    response = client.label_detection(image=image)
    labels = response.label_annotations

    # Gets first element
    return labels[9].score

if __name__ == '__main__':
