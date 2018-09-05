import classify
import PhotoCtrl
import PiConf
import sys
from subprocess import Popen, PIPE

import json



class ClassifyCtrl:

    def classify_photo(self, img):
        path = PiConf.PHOTO_PATH + "/" + img + ".jpg"
        return self.do_classify(path)


    def do_classify(self, path):
        return classify.classify(path)


def createClassifyCtrl():
    return ClassifyCtrl()


if __name__ == '__main__':
    D = createClassifyCtrl()
    if len(sys.argv) > 1:
        rc = D.do_classify(sys.argv[1])
        print rc
    else:
        P = PhotoCtrl.createPhotoCtrl()
        photos = P.get_list()
        if len(photos) > 0:
            p = photos[-1]
            rc = D.do_classify(p)
            print rc