import cv2 as cv
import tf_labels
import PiConf


def detectPic(img_path, thr=0.3):
    img = cv.imread(img_path)
    cvNet = cv.dnn.readNetFromTensorflow(PiConf.DNN_PATH, PiConf.DNN_TXT_PATH)

    #img = cv.imread('270.jpg')
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
            #print(tf_labels.getLabel(int(detection[1])), score, left, top, right, bottom)
            #cv.rectangle(img, (int(left), int(top)), (int(right), int(bottom)), (23, 230, 210), thickness=2)
    print ret
    return img, ret


if __name__ == '__main__':

    d = detectPic('floyd_1.jpg')
    print d