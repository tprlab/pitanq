import MotorCtrl
import PhotoCtrl
import PiConf

import logging
import track_cv as track
import time
import numpy as np
import traceback
import math
import track_conf as tconf
from datetime import datetime
import os

class FollowLineCtrl:

    motor_ctrl = None
    photo_ctrl = None

    max_iter = 100

    last_turn = 0
    last_angle = 0 

    photo_n = 0

    path = ""
    iter_n = 0

    track_id = None
    last_photo_path = None

    def next(self):
        self.iter_n += 1
        return self.iter_n < self.max_iter


    def __init__(self, motor, photo):
        self.motor_ctrl = motor
        self.photo_ctrl = photo


    def init(self):
        self.photo_n = 0
        self.iter_n = 0
        self.track_id = self.get_id()
        self.path = PiConf.PHOTO_PATH + "/track/" + self.track_id
        if not os.path.isdir(self.path):
            os.makedirs(self.path)
        return self.track_id



    def follow(self):
        if not self.track_id:
            self.init()

        self.motor_ctrl.set_motors("f", "f")   
        self.last_turn = 0
        self.last_angle = 0 

        try:
            while(self.next()):
                if not self.follow_step(self.iter_n):
                    break
        finally:
            self.motor_ctrl.set_motors("s", "s")



    def follow_step(self, i):
        a, shift = self.get_vector()
        if a is None:
            if self.last_turn != 0:
                a, shift = self.find_line(self.last_turn)
                if a is None:
                    return False
            elif self.last_angle != 0:
                logging.debug(("Looking for line by angle", self.last_angle))
                self.turn(np.sign(90 - self.last_angle), tconf.turn_step)
                return True
            else:
                return False

        logging.debug((i, "Angle", a, "Shift", shift))

        turn_state, shift_state = track.check_shift_turn(a, shift)

        turn_dir, turn_val = track.get_turn(turn_state, shift_state)

        if turn_dir != 0:
            self.turn(turn_dir, turn_val)
            self.last_turn = turn_dir
        else:
            time.sleep(tconf.straight_run)
            self.last_turn = 0
        self.last_angle = a
        return True


    def find_line(self, side):
        logging.debug (("Finding line", side))
        if side == 0:
            return None, None
            
        for i in xrange(0, tconf.find_turn_attempts):
            self.turn(side, tconf.find_turn_step)
            angle, shift = self.get_vector()
            if angle is not None:
                return angle, shift

        return None, None

    def get_photo(self):
        rc, phid = self.photo_ctrl.make_photo()
        if rc  == False:
            return False, None, None
        fpath, fname = self.photo_ctrl.get_path(phid)
        if fpath is None:
            return False, None, None
        self.photo_n += 1
        return True, phid, fpath + "/" + fname

    def get_photo_path(self):
        return "{0}/{1}.jpg".format(self.path, self.photo_n)

    def get_track_photo_path(self, track, photo):
        return "{0}/track/{1}".format(PiConf.PHOTO_PATH, track), "{}.jpg".format(photo)


    def get_last_photo(self):
        return None if self.last_photo_path is None else self.last_photo_path[len(PiConf.PHOTO_PATH) + 1:-4]

    def get_vector(self):
        rc, phid, fname = self.get_photo()
        if not rc:
            return None, None
        print self.path, " -- ", self.photo_n
        self.last_photo_path = self.get_photo_path()
        angle, shift = track.handle_pic(fname, fout=self.last_photo_path)
        return angle, shift


    def turn(self, r, t):
        turn_cmd = "s0" if r > 0 else "0s"
        ret_cmd = "f0" if r > 0 else "0f"
        turn = "Right" if r > 0 else "Left"
        logging.debug(("Turn", turn, t))
        self.motor_ctrl.set_motors(turn_cmd[0], turn_cmd[1])
        time.sleep(t)
        self.motor_ctrl.set_motors(ret_cmd[0], ret_cmd[1])


    def get_id(self):
        return datetime.now().strftime('%d%m%Y%H%M%S')

            

if __name__ == '__main__':

    motor_ctrl = MotorCtrl.createMotorCtrl()
    photo_ctrl = PhotoCtrl.createPhotoCtrl()

    f = FollowLineCtrl(motor_ctrl, photo_ctrl)
    f.follow()