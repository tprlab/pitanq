import PhotoCtrl
import detect
import logging
import PiConf

class HaarDetectCtrl:

    cascade = PiConf.CAT_CASCADE

    def structure(self,rects):
        if rects is None:
            return []
        ret = []
        for r in rects:
            if len(r) < 4:
                continue
            R = {"x" : r[0], "y" : r[1], "w" : r[2], "h" : r[3]}
            ret.append(R)
        logging.debug(ret)
        return ret


    def do_detect(self, img):
        path = PiConf.PHOTO_PATH + "/" + img + ".jpg"
        pic, rects = detect.handleFile(path, self.cascade)
        logging.debug("Detected on" + img + ": " + str(rects))
        return self.structure(rects)
            



def createDetectCtrl():
    return HaarDetectCtrl()


if __name__ == '__main__':
    D = createDetectCtrl()
    P = PhotoCtrl.createPhotoCtrl()
    photos = P.get_list()
    if len(photos) > 0:
        p = photos[-1]
        p = "floyd_1"
        rc = D.do_detect(p)
        print rc