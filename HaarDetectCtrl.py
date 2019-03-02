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

    def detect_file(self, path):
        pic, rects = detect.handleFile(path, self.cascade)
        logging.debug("Detected on" + path + ": " + str(rects))
        return self.structure(rects)



    def do_detect(self, img):
        path = PiConf.PHOTO_PATH + "/" + img + ".jpg"
        return self.detect_file(path)
            



def createDetectCtrl():
    return HaarDetectCtrl()


if __name__ == '__main__':
    D = createDetectCtrl()
    p = "test/data/cat.jpg"
    rc = D.detect_file(p)
    print (rc)