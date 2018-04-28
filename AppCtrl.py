import MotorCtrl
import PhotoCtrl
import stand
import HaarDetectCtrl
import DnnDetectCtrl
import DistCtrl

import socket


class AppCtrl:

    motor_ctrl = None
    photo_ctrl = None
    stand_ctrl = None
    haar_ctrl = None
    dnn_ctrl = None
    dist_ctrl = None

    def __init__(self):
        self.motor_ctrl = MotorCtrl.createMotorCtrl()
        self.photo_ctrl = PhotoCtrl.createPhotoCtrl()
        self.stand_ctrl = stand.createStandCtrl()
        self.dist_ctrl = DistCtrl.createDistCtrl()
        self.haar_ctrl = HaarDetectCtrl.createDetectCtrl()
        self.dnn_ctrl = DnnDetectCtrl.createDetectCtrl()



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





def createCtrl():
    return AppCtrl()






    