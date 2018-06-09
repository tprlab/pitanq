import PhotoCtrl
import dnn_detect
import logging
import PiConf

class DnnDetectCtrl:


    def do_detect(self, img):
        path = PiConf.PHOTO_PATH + "/" + img + ".jpg"
        pic, rects = dnn_detect.detectPic(path)
        logging.debug("Detected on" + img + ": " + str(rects))
        return rects
            



def createDetectCtrl():
    return DnnDetectCtrl()


if __name__ == '__main__':
    D = createDetectCtrl()
    P = PhotoCtrl.createPhotoCtrl()
    photos = P.get_list()
    if len(photos) > 0:
        p = photos[-1]
        print "Detecting photo", p
        rc = D.do_detect(p)
        print rc