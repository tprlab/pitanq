import classify
import PhotoCtrl
import PiConf
import sys
from subprocess import Popen, PIPE
import os
import json
from datetime import datetime
import logging



class ClassifyCtrl:

    def classify_photo(self, img):
        path = PiConf.PHOTO_PATH + "/" + img + ".jpg"
        return self.classify_ex(path)


    def do_classify(self, path):
        return classify.classify(path)

    def get_file_id(self):
        return datetime.now().strftime('%d%m%Y%H%M%S')


    def classify_ex(self, path):
        tmp_path = PiConf.TMP_DIR + "/tf"
        if not os.path.exists(tmp_path):
            os.makedirs(tmp_path)

        outpath = tmp_path + "/" + self.get_file_id() + ".json"
        process = Popen([PiConf.PYTHON_PROCESS, PiConf.PITANQ_HOME + "/classify.py", path, outpath], stdout=PIPE)
        (output, err) = process.communicate()
        exit_code = process.wait()
        if not os.path.exists(outpath):
            logging.debug(("No output file for TF classifier", outpath))
            return None
        ret = None
        with open(outpath, "r") as f:
            ret = json.load(f)
        return ret



def createClassifyCtrl():
    return ClassifyCtrl()


if __name__ == '__main__':
    D = createClassifyCtrl()
    p = "test/data/detect.jpg"
    rc = D.classify_ex(p)
    print (rc)
