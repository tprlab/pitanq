import cv2 as cv
import tf_labels
import PiConf
import sys

tf_labels.initLabels(PiConf.DNN_LABELS_PATH)

def detectPic(img_path, thr=0.3):
    img = cv.imread(img_path)
    cvNet = cv.dnn.readNetFromTensorflow(PiConf.DNN_PATH, PiConf.DNN_TXT_PATH)

    rows = img.shape[0]
    cols = img.shape[1]
    cvNet.setInput(cv.dnn.blobFromImage(img, 1.0/127.5, (300, 300), (127.5, 127.5, 127.5), swapRB=True, crop=False))
    cvOut = cvNet.forward()
    ret = []

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
            ret.append(a)
    #print (ret)
    return img, ret


if __name__ == '__main__':

    d = detectPic(sys.argv[1])
    print (d)