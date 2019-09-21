import PiConf
import logging
import time
import numpy as np
import traceback
import math
from datetime import datetime
import os
import walk_conf as wconf
from tf_walk import TFWalkClassifier
import cv2 as cv
import RoadMask

MAX_STEP_ATTEMPT = 2

class RoadClass:


    rmask = None
    tfc = None

    def __init__(self, rcname = None):
        self.tfc = TFWalkClassifier()
        logging.debug("Initializing TF...")
        self.tfc.init()
        logging.debug("TF inited")

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

        c = self.tfc.classify(mask)
        logging.debug(("Classified as", c))
        if c is None:
            return None
        ret = 0
        if c == TFWalkClassifier.TF_LEFT:
            ret = -1
        if c == TFWalkClassifier.TF_RIGHT:
            ret = 1
        
        return ret

    def get_out_path(self):
        return self.rmask.get_out_path()



if __name__ == '__main__':

    log_file = "/home/pi/test.log"
    logging.basicConfig(filename=log_file,level=logging.DEBUG, format='%(asctime)s.%(msecs)03d %(threadName)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')


    rc = RoadClass()
    f_path = "test/data/road.jpg"    
    g_path = "test/data/road_wmask.jpg"    
    rc.prepare(f_path)
    c = rc.classify(f_path, g_path)

    print ("Predict", c)