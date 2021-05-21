# USAGE
# python test_anomaly_detector.py --model anomaly_detector.model --image examples/highway_a836030.jpg
#  python test_anomaly_video_detector.py --model alexcrue_anomaly.model -i V_101.mp4  
# import the necessary packages
from pyimagesearch.features import quantify_image
import argparse
import pickle
import cv2

# construct the argument parser and parse the arguments
# ap = argparse.ArgumentParser()
# ap.add_argument("-m", "--model", required=True,
# 	help="path to trained anomaly detection model")
# ap.add_argument("-i", "--image", required=True,
# 	help="path to input image")
# args = vars(ap.parse_args())

# load the anomaly detection model

cam = cv2.VideoCapture('V_101.mp4')
print("[INFO] loading anomaly detection model...")
model = pickle.loads(open("alexcrue_anomaly.model", "rb").read())

# load the input image, convert it to the HSV color space, and
# quantify the image in the *same manner* as we did during training

# image = cv2.imread(args["image"])


while(1):
	ret, frame = cam.read()
	image = frame
	hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
	features = quantify_image(hsv, bins=(3, 3, 3))



	preds = model.predict([features])[0]
	label = "anomaly" if preds == -1 else "normal"
	color = (0, 0, 255) if preds == -1 else (0, 255, 0)

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

# draw the predicted label text on the original image
	cv2.putText(image, label, (10,  25), cv2.FONT_HERSHEY_SIMPLEX,0.7, color, 2)

# display the image
	cv2.imshow("Output", image)
# cv2.waitKey(0)
cam.release()
cv2.destroyAllWindows()