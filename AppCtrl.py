import MotorCtrl
import PhotoCtrl
import stand
import HaarDetectCtrl
import DnnDetectCtrl
import DistCtrl
import subprocess
import PiConf
import ClassifyCtrl
import MTFollowLineCtrl
import MTWalkCtrl
import GpsCtrl
import GpsUtil
import MTNavCtrl

import socket
import os
import logging



class AppCtrl:

    motor_ctrl = None
    photo_ctrl = None
    stand_ctrl = None
    haar_ctrl = None
    dnn_ctrl = None
    dist_ctrl = None
    class_ctrl = None
    line_ctrl = None
    walk_ctrl = None
    gps_ctrl = None
    nav_ctrl = None
    mock_gps_ctrl = None

    mock_gps = False

    def __init__(self):
        self.motor_ctrl = MotorCtrl.createMotorCtrl()
        self.photo_ctrl = PhotoCtrl.createPhotoCtrl()
        self.stand_ctrl = stand.createStandCtrl()
        self.dist_ctrl = DistCtrl.createDistCtrl()
        self.haar_ctrl = HaarDetectCtrl.createDetectCtrl()
        self.dnn_ctrl = DnnDetectCtrl.createDetectCtrl()
        self.class_ctrl = ClassifyCtrl.createClassifyCtrl()
        self.line_ctrl = MTFollowLineCtrl.MTFollowLineCtrl(self.motor_ctrl, self.photo_ctrl)
        self.walk_ctrl = MTWalkCtrl.createWalkCtrl(self.motor_ctrl, self.photo_ctrl)
        self.gps_ctrl = GpsCtrl.createGpsCtrl()
        self.nav_ctrl = MTNavCtrl.createNavCtrl()

        self.nav_ctrl.init(self.gps_ctrl, self.motor_ctrl)

        self.mock_gps_ctrl = GpsCtrl.createMockGpsCtrl()
        self.mock_gps_ctrl.setPoint(GpsUtil.nyc_pos)

        if not os.path.exists(PiConf.TMP_DIR):
            os.makedirs(PiConf.TMP_DIR)


    def ping(self):
        return {"rc" : "1"}

    def name(self):
        return {"name" : socket.gethostname()}


    def fwd_on(self):
        return {"rc": self.motor_ctrl.fwd_on()}

    def fwd_off(self):
        return {"rc" : self.motor_ctrl.fwd_off()}

    def back_on(self):
        return {"rc" : self.motor_ctrl.back_on()}

    def back_off(self):
        return {"rc" : self.motor_ctrl.back_off()}

    def right_on(self):
        return {"rc" : self.motor_ctrl.right_on()}

    def right_off(self):
        return {"rc" : self.motor_ctrl.right_off()}

    def left_on(self):
        return {"rc" : self.motor_ctrl.left_on()}

    def left_off(self):
        return {"rc" : self.motor_ctrl.left_off()}

    def set_motors(self, r, l):
        rc, lc = self.motor_ctrl.set_motors(r, l)
        return {"r" : rc, "l" : lc}



    def make_photo(self):
        rc, info = self.photo_ctrl.make_photo()
        ret = {"rc" : rc}
        if rc:
            ret["name"] = info
        else:
            ret["err"] = info
        return ret



    def getPhotoPath(self, phid):
        return self.photo_ctrl.get_path(phid)

    def getPhotosList(self):
        return self.photo_ctrl.get_list()

    def cam_up(self):
        return {"rc" : self.stand_ctrl.up()}

    def cam_down(self):
        return {"rc" : self.stand_ctrl.down()}

    def cam_left(self):
        return {"rc" : self.stand_ctrl.left()}

    def cam_right(self):
        return {"rc" : self.stand_ctrl.right()}

    def detect_dnn(self, ph):
        return self.dnn_ctrl.do_detect(ph)

    def detect_haar(self, ph):
        return self.haar_ctrl.do_detect(ph)
    def dist(self):
        return self.dist_ctrl.distance()


    def update(self):
        p = subprocess.Popen(["git", "pull"], cwd=PiConf.PITANQ_HOME, stdout=subprocess.PIPE)
        out,err = p.communicate()
        return {"rc" : p.returncode, "info":out}
            
    def classify(self, phid):
        return self.class_ctrl.classify_photo(phid)

    def start_follow(self):
        return self.line_ctrl.start_follow()

    def stop_follow(self):
        return self.line_ctrl.stop_follow()

    def get_follow_photo(self):
        return self.line_ctrl.get_last_photo()

    def get_track_photo_path(self, track, photo):
        return self.line_ctrl.get_track_photo_path(track, photo)

    def get_follow_id(self):
        return self.line_ctrl.track_id

    def prepare_follow(self):
        a, s = self.line_ctrl.prepare_follow()
        return {"angle" : a, "shift" : s}

    def prepare_walk(self):
        rc = self.walk_ctrl.prepare_action()
        return {"rc" : rc}

    def get_walk_photo(self):
        return self.walk_ctrl.get_action_pic()


    def start_walk(self):
        return self.walk_ctrl.start_follow()

    def stop_walk(self):
        return self.walk_ctrl.stop_follow()

    def get_mock_gps(self):
        return self.mock_gps_ctrl.get_coords()

    def get_gps(self):
        gps = self.gps_ctrl if self.mock_gps == False else self.mock_gps_ctrl
        g = gps.get_coords()
        if g is None:
            return {}
        logging.debug(("Returned gps", g))
        return g

    def start_nav(self, target):
        if self.mock_gps == False:
            rc = self.nav_ctrl.start_nav(target)
            return {"rc" : rc}

        self.mock_gps_ctrl.setPoint(target)

        return {"rc" : True}
        

    def stop_nav(self):
        if self.mock_gps == False:
            return {"rc" : True}
            
        rc = self.nav_ctrl.stop_nav()
        return {"rc" : rc}

        




def createCtrl():
    return AppCtrl()



if __name__ == '__main__':
    app = createCtrl()
    print (app.update())


    