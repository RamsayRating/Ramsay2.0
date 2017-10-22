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
    return labels[0].score

def stars(img_name):
    corr_val = what_object(img_name)
    star = 0

    if (corr_val <= .6):
        return(1, corr_val)
        #print("1 Star")
    elif (.6 < corr_val) and (corr_val <= .7):
        return(2, corr_val)
        #print("2 Star")
    elif (.7 < corr_val) and (corr_val <= .8):
        return(3, corr_val)
        #print("3 Star")
    elif (.8 < corr_val) and (corr_val <= .9):
        return(4, corr_val)
        #print("4 Star")
    else:
        return(5, corr_val)
        #print("5 Star")

if __name__ == '__main__':
    star_val, corr_val = stars('RedApple.jpg')
    print('Top score: ' + str(corr_val))
    print('Star Value: ' + str(star_val))
