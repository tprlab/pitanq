import PhotoCtrl
import dnn_detect
import logging
import PiConf

class DnnDetectCtrl:

    def detect_file(self, path):
        pic, rects = dnn_detect.detectPic(path)
        logging.debug("Detected on" + path + ": " + str(rects))
        return rects


    def do_detect(self, img):
        path = PiConf.PHOTO_PATH + "/" + img + ".jpg"
        return self.detect_file(path)
            



def createDetectCtrl():
    return DnnDetectCtrl()


if __name__ == '__main__':
    D = createDetectCtrl()
    p = "test/data/detect.jpg"
    rc = D.detect_file(p)
    print (rc)