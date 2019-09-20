MOTOR_RF = 40
MOTOR_RB = 38

MOTOR_LF = 36
MOTOR_LB = 32

DIST_TRIGGER = 37
DIST_ECHO = 35

VERSION = 4.0


DNN_PATH = "/home/pi/ssd_mobilenet_v1_coco_11_06_2017/frozen_inference_graph.pb"
#DNN_PATH = "/home/pi/ssd_mobilenet_v1_coco_2018_01_28/frozen_inference_graph.pb"

DNN_TXT_PATH = "/home/pi/opencv-extra/ssd_mobilenet_v1_coco.pbtxt"

DNN_LABELS_PATH = "/home/pi/opencv-extra/mscoco_label_map.pbtxt"

CAT_CASCADE = "/home/pi/opencv-extra/haarcascades/haarcascade_frontalcatface.xml"

PHOTO_PATH="/home/pi/pitanq/photos"

LOG_PATH = "/home/pi/pitanq/logs"
LOG_FILE = "robot.log"

PITANQ_HOME = "/home/pi/pitanq"


IMAGENET_MODEL_DIR = "/home/pi/imagenet"

TMP_DIR = "/home/pi/pitanq/tmp"
PYTHON_PROCESS = "/usr/bin/python3"

SEGMENT_MODEL = "/home/pi/enet-cityscapes/enet-model.net"
SEGMENT_CLASSES = "/home/pi/enet-cityscapes/enet-classes.txt"
SEGMENT_COLORS = "/home/pi/enet-cityscapes/enet-colors.txt"

NCS_MODEL_XML = "/home/pi/ncs_models/road-segmentation-adas-0001.xml"
NCS_MODEL_BIN = "/home/pi/ncs_models/road-segmentation-adas-0001.bin"
NCS_DEVICE = "MYRIAD"
NCS_PLUGIN_PATH = "/opt/intel/openvino/inference_engine/lib/armv7l"

DRIVE_CLASSIFIER_KERAS_JSON = "/home/pi/drive_nn/model.json"
DRIVE_CLASSIFIER_KERAS_MODEL = "/home/pi/drive_nn/model.h5"

DRIVE_CLASSIFIER_NCS_XML = "/home/pi/drive_nn/ktf_model.xml"
DRIVE_CLASSIFIER_NCS_BIN = "/home/pi/drive_nn/ktf_model.bin"


ROAD_IMPL = "ncs"

NCS_DETECT_XML = "/home/pi/ssd_ncs/frozen_inference_graph.xml"
NCS_DETECT_BIN = "/home/pi/ssd_ncs/frozen_inference_graph.bin"

INCEPTION_LABELS = "/home/pi/inception/labels.txt"
NCS_INCEPTION_XML = "/home/pi/inception/inception_v4_inference_graph.xml"
NCS_INCEPTION_BIN = "/home/pi/inception/inception_v4_inference_graph.bin"