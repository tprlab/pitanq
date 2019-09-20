import sys, os
import numpy as np
from time import time
import cv2 as cv
import logging
import PiConf
import tf_labels
import colormap
from ncs_wrapper import NcsWrapper


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

tf_labels.initLabels(PiConf.DNN_LABELS_PATH)

def get_detect_from_tensor(t, rows, cols):
    score = t[2]
    cls = int(t[1])
    left = int(t[3] * cols)
    top = int(t[4] * rows)
    right = int(t[5] * cols)
    bottom = int(t[6] * rows)
    name = tf_labels.getLabel(cls)

    return {"name" : name, "class" : cls, "score" : score, "x" : left, "y" : top, "w" : (right - left), "h" : (bottom - top)}


class NcsDetector(NcsWrapper):

    def init(self):
        model, net = self.load_model_base(PiConf.NCS_DETECT_XML, PiConf.NCS_DETECT_BIN)
        return model is not None


    def detect(self, image):
        data = self.run(image, True)
        return None if data is None else data[0]


def build_detection(data, thr, rows, cols):
    T = {}
    for t in data:
        score = t[2]
        if score > thr:
            cls = int(t[1])
            if cls not in T:
                T[cls] = get_detect_from_tensor(t, rows, cols)
            else:
                a = T[cls]
                if a["score"] < score:
                    T[cls] = get_detect_from_tensor(t, rows, cols)
    return T.values()

def draw_detections(D, img, out):
    n = 0

    for a in D:
        clr = colormap.get_color(n)
        n += 1
        cv.rectangle(img, (a["x"], a["y"], a["x"] + a["w"], a["y"] + a["h"]), clr, thickness=2)
        word = a["name"] + "(" + str(int(100. * a["score"])) + "%)" 
        cv.putText(img, word, (a["x"] + 5, a["y"] + 25), cv.FONT_HERSHEY_SIMPLEX, 1, clr, 2, cv.LINE_AA)
    cv.imwrite(out, img)


def print_detections(D):
    for a in D:
        print(a)



if __name__ == '__main__':
    nc = NcsDetector()
    nc.init()
    path = sys.argv[1]
    img = cv.imread(path)
    rows = img.shape[0]
    cols = img.shape[1]

    data = nc.detect(img)

    thr = 0.3

    d = build_detection(data, thr, rows, cols)

    print_detections(d)

    if len(sys.argv) > 2:
        out = sys.argv[2]
        draw_detections(d, img, out)
