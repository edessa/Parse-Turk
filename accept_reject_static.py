import pandas as pd
import requests
import numpy as np
from PIL import Image
import cv2
import json


files = pd.read_csv('./Annotations/Epic-Kitchens-Batch-Round-1.csv').to_dict()

print(files.keys())
print(files['Approve'], files['Reject'], files['Input.image_url'])

accept = files['Approve']
reject = files['Reject']

images = files["Input.image_url"]
annotations = files["Answer.annotatedResult.polygons"]

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
	#cv2.imwrite(/home/lab/Annotations/poly-annotations/' + str(i) + '.png', img)
	cv2.imshow('Hand-Polygon Annotations', img)
	res = cv2.waitKey(0)
	if res == ord('a'):
		accept[i] = True
	elif res == ord('r'):
		reject[i] = True

print(accept, reject)

files['Approve'] = accept
files['Reject'] = reject

pd.DataFrame(files).to_csv('./Annotations/50-Salads-Hand-Polygons-Checked.csv', index=False)
