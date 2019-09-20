import sys
import numpy as np
from time import time
import cv2 as cv
import PiConf
import logging
import ncs_core as ncs

colors = [
    (0, 0, 0),
    (255, 255, 255),
    (255, 0, 0),
    (0, 255, 0)
]

colors = np.array(colors, dtype="uint8")


def load_segment_model():
    model_xml = PiConf.NCS_MODEL_XML
    model_bin = PiConf.NCS_MODEL_BIN

    if ncs.init_ncs() is None:
        return None, None
    return ncs.load_ncs_model(model_xml, model_bin)

def segment_image(image_path, seg_model, seg_net):

    input_blob = next(iter(seg_model.inputs))
    out_blob = next(iter(seg_model.outputs))

    n, c, h, w = seg_model.inputs[input_blob].shape

    image0 = cv.imread(image_path)
    image = cv.resize(image0, (w, h))
    image = image.transpose((2, 0, 1))  # Change data layout from HWC to CHW
    data = ncs.run_ncs(seg_model, seg_net, image)
    d0 = np.argmax(data, axis=0)
    mask = colors[d0]


    full_mask = cv.resize(mask, (image0.shape[1], image0.shape[0]),interpolation=cv.INTER_NEAREST)
    classMap = cv.resize(d0, (image0.shape[1], image0.shape[0]), interpolation=cv.INTER_NEAREST)
    gmask = cv.resize(mask, (64, 64))
    gmask = cv.cvtColor(gmask, cv.COLOR_BGR2GRAY)


    output = ((0.6 * image0) + (0.4 * full_mask)).astype("uint8")

    return output, gmask



if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    image_path = "test/data/road.jpg"
    model, net = load_segment_model()
    if net is not None:
        out, mask = segment_image(image_path, model, net)
        cv.imwrite("test/data/road-seg-mask.jpg", mask)
        cv.imwrite("test/data/road-seg-ncs-out.jpg", out)
    else:
        print("Segmentation model not loaded")

