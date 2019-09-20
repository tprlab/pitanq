import sys, os
import numpy as np
from time import time
import cv2 as cv
import logging
import ncs_core as ncs


class NcsWrapper:
    model = None
    net = None

    def load_model_base(self, xml_path, bin_path):
        if ncs.init_ncs() is None:
            return None, None
        self.model, self.net = ncs.load_ncs_model(xml_path, bin_path)
        return self.model, self.net

    def run(self, image, trans = False):
        if image is None:
            return None

        input_blob = next(iter(self.model.inputs))
        out_blob = next(iter(self.model.outputs))

        n, c, h, w = self.model.inputs[input_blob].shape

        if image.shape != (h,w):
            image = cv.resize(image, (w, h))
        if trans:
            image = image.transpose((2, 0, 1))
    
        return ncs.run_ncs(self.model, self.net, image)

