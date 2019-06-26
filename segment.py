import numpy as np
import argparse
import time
import cv2
import PiConf
import logging

def load_segment_model():
    try:
        classes = None
        with open(PiConf.SEGMENT_CLASSES) as f:
            classes = f.read().strip().split("\n")
        colors = None
        with open(PiConf.SEGMENT_COLORS) as f:
            colors= f.read().strip().split("\n")
        colors = [np.array(c.split(",")).astype("int") for c in colors]
        colors = np.array(colors, dtype="uint8")
        print("[INFO] loading model...")
        net = cv2.dnn.readNet(PiConf.SEGMENT_MODEL)
        return net, classes, colors
    except Exception as e:
        logging.exception("Cannot load segment model")
    return None, None, None

def segment_image(image_path, seg_net, seg_classes, seg_colors):

    image0 = cv2.imread(image_path)
    image = cv2.resize(image0, (1024, 512),interpolation=cv2.INTER_NEAREST)
    blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (1024, 512), 0, swapRB=True, crop=False)

    seg_net.setInput(blob)
    start = time.time()
    output = seg_net.forward()
    end = time.time()


    print("[INFO] inference took {:.4f} seconds".format(end - start))

    (numClasses, height, width) = output.shape[1:4]

    classMap = np.argmax(output[0], axis=0)

    mask = seg_colors[classMap]

    mask = cv2.resize(mask, (image0.shape[1], image0.shape[0]),interpolation=cv2.INTER_NEAREST)
    classMap = cv2.resize(classMap, (image0.shape[1], image0.shape[0]), interpolation=cv2.INTER_NEAREST)

    gmask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
    gmask = cv2.resize(gmask, (128, 64), interpolation=cv2.INTER_NEAREST)
    gmask = gmask[0:64,32:96]


    output = ((0.6 * image0) + (0.4 * mask)).astype("uint8")

    #cv2.imwrite("mask.jpg", gmask)
    #cv2.imwrite("out.jpg", output)
    return output, gmask



if __name__ == '__main__':
    image_path = "test/data/road.jpg"
    net, cls, clr = load_segment_model()
    if net is not None:
        out, mask = segment_image(image_path, net, cls, clr)
        cv2.imwrite("test/data/road-seg-mask.jpg", mask)
        cv2.imwrite("test/data/road-seg-out.jpg", out)
    else:
        print("Segmentation model not loaded")

