import cv2 as cv
import tf_labels
import PiConf
import sys
from time import time
import logging
import colormap

tf_labels.initLabels(PiConf.DNN_LABELS_PATH)

def detectPic(img_path, thr=0.3):
    img = cv.imread(img_path)
    t0 = time()
    cvNet = cv.dnn.readNetFromTensorflow(PiConf.DNN_PATH, PiConf.DNN_TXT_PATH)
    t1 = time()
    logging.debug("DNN model read in {:.4f} seconds".format(t1 - t0))
    cvNet.setPreferableBackend(cv.dnn.DNN_BACKEND_OPENCV)
    cvNet.setPreferableTarget(cv.dnn.DNN_TARGET_CPU)


    rows = img.shape[0]
    cols = img.shape[1]
    cvNet.setInput(cv.dnn.blobFromImage(img, 1.0/127.5, (300, 300), (127.5, 127.5, 127.5), swapRB=True, crop=False))
    t0 = time()
    cvOut = cvNet.forward()
    t1 = time()
    logging.debug("DNN model made inference in {:.4f} seconds".format(t1 - t0))

    ret = []

    print("Shape", cvOut.shape)
    #print(cvOut)
    for detection in cvOut[0,0,:,:]:
        score = float(detection[2])
        if score > thr:
            left = detection[3] * cols
            top = detection[4] * rows
            right = detection[5] * cols
            bottom = detection[6] * rows
            cls = int(detection[1])
            a = {}
            a["class"] = cls
            a["name"] = tf_labels.getLabel(cls)
            a["score"] = score
            a["x"] = int(left)
            a["y"] = int(top)
            a["w"] = int(right - left)
            a["h"] = int(bottom - top)
            print(a)
            ret.append(a)
    #print (ret)
    return img, ret


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    img, d = detectPic(sys.argv[1])
    out = None if len(sys.argv) < 3 else sys.argv[2]
    
    n = 0
    for a in d:
        print(a)
        if out is not None:
            clr = colormap.get_color(n)
            n += 1
            cv.rectangle(img, (a["x"], a["y"], a["x"] + a["w"], a["y"] + a["h"]), clr, thickness=2)
            word = a["name"] + "(" + str(int(100. * a["score"])) + "%)" 
            cv.putText(img, word, (a["x"] + 5, a["y"] + 25), cv.FONT_HERSHEY_SIMPLEX, 1, clr, 2, cv.LINE_AA)
    cv.imwrite(out, img)


            
