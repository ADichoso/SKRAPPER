# Some of the code is copied from Google's example at
# https://github.com/tensorflow/models/blob/master/research/object_detection/object_detection_tutorial.ipynb

# and some is copied from Dat Tran's example at
# https://github.com/datitran/object_detector_app/blob/master/object_detection_app.py

# how to run
# python Object_detection_webcam.py --modelName inference_graph/A --threshold 0.6
import os
import cv2
import sys
import time
import numpy as np
import tensorflow as tf

sys.path.append("..")
import argparse
from utils import label_map_util
from utils import visualization_utils as vis_util


parser = argparse.ArgumentParser(description='setup for object detection')

parser.add_argument('--modelName', type=str, help='inference graph directory')
parser.add_argument('--threshold', type=float, default=0.6, help='directory')

args = parser.parse_args()

MODEL_NAME = args.modelName
THRESHOLD = args.threshold

CWD_PATH = os.getcwd()  #current working directory
PATH_TO_LABELS = os.path.join(CWD_PATH, 'mobilenet_v1_0.75_224_quant', 'labelmap.pbtxt')
PATH_TO_CKPT = os.path.join(CWD_PATH, MODEL_NAME, 'frozen_inference_graph.pb')

NUM_CLASSES = 23

FONT = cv2.FONT_HERSHEY_SIMPLEX
FILL = cv2.FILLED

# Load the label map
label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)


# Load the Tensorflow model into memory
detection_graph = tf.Graph()
with detection_graph.as_default():
	od_graph_def = tf.GraphDef()
	with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
		serialized_graph = fid.read()
		od_graph_def.ParseFromString(serialized_graph)
		tf.import_graph_def(od_graph_def, name='')

	sess = tf.Session(graph=detection_graph)

	image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')		# Input tensor is the image

	detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
	detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
	detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')

	num_detections = detection_graph.get_tensor_by_name('num_detections:0')

cam = cv2.VideoCapture(0)
cam.set(3, 1280)
cam.set(4, 720)

while True:
	time_init = time.time()

	ret, frame = cam.read()
	frame = cv2.flip(frame, 1)
	frame_expanded = np.expand_dims(frame, axis=0)

	(boxes, scores, classes, num) = sess.run(
		[detection_boxes, detection_scores, detection_classes, num_detections],
		feed_dict={image_tensor: frame_expanded})

	vis_util.visualize_boxes_and_labels_on_image_array(
		frame,
		np.squeeze(boxes),
		np.squeeze(classes).astype(np.int32),
		np.squeeze(scores),
		category_index,
		use_normalized_coordinates=True,
		line_thickness=5,
		min_score_thresh=THRESHOLD)

	sec = time.time() - time_init

	cv2.rectangle(frame, (0, 0), (230, 65), (0, 0, 0), FILL)
	cv2.putText(frame, "[FPS : %.7s]" % (1 / sec), (0, 25), FONT, 0.8, (100, 100, 100))
	cv2.putText(frame, "[ms  : %.7s]" % (1000 * sec), (0, 55), FONT, 0.8, (100, 100, 100))

	cv2.imshow('Object detector', frame)

	if cv2.waitKey(1) == ord('q'):
		break

cam.release()
cv2.destroyAllWindows()