import classify
import PhotoCtrl
import PiConf
import sys
from subprocess import Popen, PIPE
import os
import json
from datetime import datetime



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
        process = Popen([PyConf.PYTHON_PROCESS, "classify.py", path, outpath], stdout=PIPE)
        (output, err) = process.communicate()
        exit_code = process.wait()
        return json.load(open(outpath))



def createClassifyCtrl():
    return ClassifyCtrl()


if __name__ == '__main__':
    D = createClassifyCtrl()
    if len(sys.argv) > 1:
        rc = D.classify_photo(sys.argv[1])
        print rc
    else:
        P = PhotoCtrl.createPhotoCtrl()
        photos = P.get_list()
        if len(photos) > 0:
            p = photos[-1]
            rc = D.do_classify(p)
            print rc