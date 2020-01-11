import pandas as pd
import cv2
import requests
from PIL import Image
import json
import numpy as np

files = pd.read_csv(r'C:\Users\edess\Desktop\50-Salads\50-Salads-Hand-Boxes.csv').to_dict()

print(files.keys())
images = files["Input.image_url"]
annotations = files["Answer.annotatedResult.boundingBoxes"]
print(annotations[0])

for i in range(len(images)):
    r = requests.get(images[i], stream=True)
    r.raw.decode_content = True
    img = cv2.cvtColor(np.array(Image.open(r.raw)), cv2.COLOR_RGB2BGR)
    for hand in json.loads(annotations[i]):
        print(hand.keys())
        x_1 = hand["left"]
        x_2 = hand["left"] + hand["width"]
        y_1 = hand["top"]
        y_2 = hand["top"] + hand["height"]
        cv2.rectangle(img, (x_1, y_1), (x_2, y_2), (255, 0, 0), 2)
    cv2.imwrite(r'C:\Users\edess\Desktop\50-Salads\annotations\\' + str(i) + '.png', img)
