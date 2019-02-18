from WalkCtrl import WalkCtrl
import threading
import time

import MotorCtrl
import PhotoCtrl
import PiConf


class MTWalkCtrl(WalkCtrl):

    T = None
    stop_flag = False

    def __init__(self, motor, photo):
        WalkCtrl.__init__(self, motor, photo)

    def start_follow(self):
        if self.T is None or not self.T.isAlive():
            self.stop_flag = False
            self.init()
            self.T = threading.Thread(target=self.follow)
            self.T.start()
        return self.track_id


    def stop_follow(self):
        self.stop_flag = True
        if self.T is not None:
            self.T.join()
            self.T = None
        return True

    def follow(self):
        WalkCtrl.follow(self)
        self.onDone()


    def next(self):
        if self.stop_flag:
            return False
        return WalkCtrl.next(self)

    def onDone(self):
        self.T = None

def createWalkCtrl(motor, photo):
    return MTWalkCtrl(motor, photo)


if __name__ == '__main__':

    motor_ctrl = MotorCtrl.createMotorCtrl()
    photo_ctrl = PhotoCtrl.createPhotoCtrl()

    f = MTWalkCtrl(motor_ctrl, photo_ctrl)
    f.start_follow()
    time.sleep(10)
    f.stop_follow()