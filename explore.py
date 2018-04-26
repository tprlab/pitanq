import ClassifyCtrl
import PhotoCtrl
import DistCtrl
import logging
import time
import json
import stand


logging.basicConfig(filename='/home/pi/explore.log',level=logging.DEBUG)




class ExploreCtrl:
    class_ctrl = None
    photo_ctrl = None
    dist_ctrl = None
    stand_ctrl = None

    def __init__(self):
        self.class_ctrl = ClassifyCtrl.createClassifyCtrl()
        self.photo_ctrl = PhotoCtrl.createPhotoCtrl("/home/pi/explore/photo")
        self.dist_ctrl = DistCtrl.createDistCtrl()
        self.stand_ctrl = stand.createStandCtrl()

    def cam_right(self):
        self.stand_ctrl.right();
        self.stand_ctrl.right();

    def cam_left(self):
        self.stand_ctrl.left();
        self.stand_ctrl.left();


    def start(self):
        c = self.shot()
        self.cam_right()
        r = self.shot()
        self.cam_left()
        self.cam_left()
        l = self.shot()
        self.cam_right();
        print "center", c
        print "right", r
        print "left", l


    def shot(self):    
        d = self.dist_ctrl.distance()
        rc, ph = self.photo_ctrl.make_photo()
        if rc == False:
            logging.debug("Cannot take a photo")
            return False
        logging.debug("Measured distance %f cm" % d)
        v = self.class_ctrl.classify_ex(ph)
        cls = []
        if v is not None:
            for c in v:
                score = c["score"]
                name = c["name"]
                if score >= 0.1:
                    cls.append(c)
                    logging.debug("detected %s %f" % (name, score))
                    print c
        return {"cls" : cls, "image" : ph, "dist" : d}
        


if __name__ == '__main__':    
    e = ExploreCtrl()
    e.start()        
