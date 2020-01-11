import cv2

cap = cv2.VideoCapture('./P01_11.mp4')
i = 0
increment = int(cap.size() / 100)

while cap.isOpened():
	ret, frame = cap.read()
	if i % increment == 0:
		cv2.imwrite('./frames/' + str(i) + '.png', frame)
