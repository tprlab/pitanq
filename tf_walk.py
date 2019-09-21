import sys
import os
import numpy as np
import cv2 as cv
import logging
from time import time


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


import tensorflow as tf


MODEL_JSON = "/home/pi/drive_nn/model.json"
MODEL_H5 = "/home/pi/drive_nn/model.h5"

class TFWalkClassifier:
    model = None
    graph = None
    sess = None

    def init(self):
        t0 = time()
        self.graph = tf.get_default_graph()
        self.sess = tf.Session()
        tf.keras.backend.set_session(self.sess)

        f = open(MODEL_JSON, 'r')
        model_data = f.read()
        f.close()

        self.model = tf.keras.models.model_from_json(model_data)
        self.model.load_weights(MODEL_H5)
        t1 = time()
        logging.debug("Loaded Keras model in {:.4f}".format(t1 - t0))


    def classify(self, g):
        t0 = time()
        g1 = np.reshape(g,[1,64,64,1])
        c = None
        with self.graph.as_default():
            tf.keras.backend.set_session(self.sess)            
            c = self.model.predict_classes(g1)
            #c = self.model.predict_proba(g1)
        if c is None:
            return None
        t1 = time()
        logging.debug("Classified with Keras model in {:.4f}".format(t1 - t0))
        return c[0]


if __name__ == '__main__':
    tfc = TFWalkClassifier()
    tfc.init()
    path = sys.argv[1]
    img = cv.imread(path, cv.IMREAD_GRAYSCALE)
    c = tfc.classify(img)
    print ("Classified", c)

     