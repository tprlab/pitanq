import sys, os
import numpy as np
from time import time
import cv2 as cv
import logging
import PiConf
from ncs_wrapper import NcsWrapper

if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


class NcsWalkClassifier(NcsWrapper):

    def init(self):
        self.load_model()


    def load_model(self):
        return self.load_model_base(PiConf.DRIVE_CLASSIFIER_NCS_XML, PiConf.DRIVE_CLASSIFIER_NCS_BIN)


    def classify(self, image):
        data = self.run(image)
        return None if data is None else np.argmax(data)


if __name__ == '__main__':
    nc = NcsWalkClassifier()
    nc.init()
    path = sys.argv[1]
    img = cv.imread(path, cv.IMREAD_GRAYSCALE)
    c = nc.classify(img)
    print ("Classified", c)

     
