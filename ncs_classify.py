import sys, os
import numpy as np
from time import time
import cv2 as cv
import logging
import PiConf
import inception_labels
from ncs_wrapper import NcsWrapper

if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

labels = inception_labels.init_labels(PiConf.INCEPTION_LABELS)

class NcsClassifier(NcsWrapper):


    def init(self):
        self.load_model_base(PiConf.NCS_INCEPTION_XML, PiConf.NCS_INCEPTION_BIN)

    def classify(self, image, thr):
        data = self.run(image, True)
        cont = True
        ret = []

        while(True):
            cls = np.argmax(data)
            if data[cls] < thr:
                break;
            c = {"name" : labels[cls], "class" : cls, "score" : int(100 * data[cls])}
            data[cls] = 0
            ret.append(c)
        return ret




if __name__ == '__main__':
    nc = NcsClassifier()
    nc.init()
    path = sys.argv[1]
    img = cv.imread(path)

    L = nc.classify(img, 0.1)
    for c in L:
        print(c["name"], str(c["score"]) + "%")

