import tensorflow as tf
import sys
import numpy as np
import os
import cv2 as cv


MODEL_JSON = "/home/pi/drive_nn/model.json"
MODEL_H5 = "/home/pi/drive_nn/model.h5"

class TFWalkClassifier:
    model = None
    graph = None

    TF_LEFT = 0
    TF_RIGHT = 1
    TF_STRAIGHT = 2

    def init(self):
        f = open(MODEL_JSON, 'r')
        model_data = f.read()
        f.close()

        self.model = tf.keras.models.model_from_json(model_data)
        self.model.load_weights(MODEL_H5)
        self.graph = tf.get_default_graph()

    def classify(self, g):
        g1 = np.reshape(g,[1,64,64,1])
        c = None
        with self.graph.as_default():
            c = self.model.predict_classes(g1)
            #c = self.model.predict_proba(g1)
        if c is None:
            return None
        return c[0]


if __name__ == '__main__':
    tfc = TFWalkClassifier()
    tfc.init()
    path = sys.argv[1]
    img = cv.imread(path, cv.IMREAD_GRAYSCALE)
    c = tfc.classify(img)
    print "Classified", c

     