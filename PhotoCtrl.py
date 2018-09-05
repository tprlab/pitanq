import os, os.path
import cam
from datetime import datetime
import logging
import PiConf
import subprocess



class PhotoCtrl:

    def __init__(self):
        if not os.path.isdir(PiConf.PHOTO_PATH):
            os.makedirs(PiConf.PHOTO_PATH)

    def get_file_id(self):
        return datetime.now().strftime('%d%m%Y%H%M%S')

    def make_photo(self):
        phid = self.get_file_id()
        path = os.path.join(PiConf.PHOTO_PATH, phid + ".jpg")
        logging.debug("Making photo %s" % path)
        try:
            cam.photo(path)
            return True, phid
        except Exception as e:
            logging.exception("Cannot make a photo")
            return False, e.message
        

    def get_path(self, phid):
        f = phid + ".jpg"
        path = os.path.join(PiConf.PHOTO_PATH, f)
        if os.path.exists(path):
            return PiConf.PHOTO_PATH, f  
        return None, None

    def get_list(self):
        ret = []
        for file in os.listdir(PiConf.PHOTO_PATH):
            if file.endswith(".jpg"):
                ret.append(os.path.splitext(file)[0])
        return ret


PHOTO_URL = "http://localhost:8080/?action=snapshot"


class MJPhotoCtrl(PhotoCtrl):
    def make_photo(self):
        phid = self.get_file_id()
        path = os.path.join(PiConf.PHOTO_PATH, phid + ".jpg")
        logging.debug("Making mjpeg photo %s" % path)
        try:
            subprocess.call(["wget", "-O", path, PHOTO_URL])
            return True, phid
        except Exception as e:
            logging.exception("Cannot make a photo")
            return False, e.message
       


def createPhotoCtrl():
    return MJPhotoCtrl()



if __name__ == '__main__':
    ph = createPhotoCtrl()
    ph.make_photo()