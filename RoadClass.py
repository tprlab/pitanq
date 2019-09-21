import os, sys
import PiConf
import logging
import time
import numpy as np
import traceback
import math
from datetime import datetime
import walk_conf as wconf
#from tf_walk import TFWalkClassifier
from ncs_walk import NcsWalkClassifier

import cv2 as cv
import RoadMask

MAX_STEP_ATTEMPT = 2

CLS_LEFT = 0
CLS_RIGHT = 1
CLS_STRAIGHT = 2


class RoadClass:


    rmask = None
    walk_clf = None

    def __init__(self, rcname = None):
        #self.walk_clf = TFWalkClassifier()
        self.walk_clf = NcsWalkClassifier()
        logging.debug("Initializing walk classifer...")
        self.walk_clf.init()
        logging.debug("WC inited")

        self.rmask = RoadMask.createRoadMask(rcname)
        self.rmask.init()
        logging.debug("RoadMask inited")


    def prepare(self, fpath):
        self.rmask.prepare(fpath)

    def classify(self, fpath, mask_path):
        mask = self.rmask.handle_pic(fpath, mask_path)
        if mask is None:
            logging.debug(("Cannot get road mask from", fpath))
            return None

        c = self.walk_clf.classify(mask)
        logging.debug(("Classified as", c))
        if c is None:
            return None
        ret = 0
        if c == CLS_LEFT:
            ret = -1
        if c == CLS_RIGHT:
            ret = 1
        
        return ret

    def get_out_path(self):
        return self.rmask.get_out_path()



if __name__ == '__main__':

    #log_file = "/home/pi/test.log"
    #logging.basicConfig(filename=log_file,level=logging.DEBUG, format='%(asctime)s.%(msecs)03d %(threadName)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    rc = RoadClass()
    f_path = "test/data/road.jpg"    
    g_path = "test/data/road_wmask.jpg"    
    rc.prepare(f_path)
    c = rc.classify(f_path, g_path)

    print ("Predict", c)