import pandas as pd
import cv2
import requests
from PIL import Image
import json
import numpy as np

files = pd.read_csv(r'C:\Users\edess\Desktop\50-Salads\50-Salads-Hand-Polygons.csv').to_dict()

print(files.keys())
images = files["Input.image_url"]
annotations = files["Answer.annotatedResult.polygons"]
print(annotations[0])

for i in range(len(images)):
    print(i, images[i])
    r = requests.get(images[i], stream=True)
    r.raw.decode_content = True
    img = cv2.cvtColor(np.array(Image.open(r.raw)), cv2.COLOR_RGB2BGR)
    for hand in json.loads(annotations[i]):
        pts = []
        for pt in hand["vertices"]:
            pts.append((pt["x"], pt["y"]))
        for j in range(len(pts) - 1):
            cv2.line(img, pts[j], pts[j+1], (255, 0, 0), 2)
    cv2.imwrite(r'C:\Users\edess\Desktop\50-Salads\poly-annotations\\' + str(i) + '.png', img)
