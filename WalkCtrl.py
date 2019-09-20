import MotorCtrl
import PhotoCtrl
import PiConf
import logging

if __name__ == '__main__':
    log_file = "/home/pi/test.log"
    logging.basicConfig(filename=log_file,level=logging.DEBUG, format='%(asctime)s.%(msecs)03d %(threadName)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

import time
import numpy as np
import traceback
import math
from datetime import datetime
import os
import walk_conf as wconf
import cv2 as cv
import RoadClass


MAX_STEP_ATTEMPT = 2


class PreWalkCtrl:
    photo_ctrl = None
    rclass = None

    last_phid = None

    last_g_path = None
    last_s_path = None
    last_p_path = None


    def __init__(self, photo, rclass):
        self.photo_ctrl = photo
        self.rclass = rclass if rclass is not None else RoadClass.RoadClass(PiConf.ROAD_IMPL)


    def get_photo(self):
        logging.debug("Make walk photo")
        rc, phid = self.photo_ctrl.make_photo()
        if rc  == False:
            return False, None, None
        fpath, fname = self.photo_ctrl.get_path(phid)
        if fpath is None:
            return False, None, None
        return True, phid, fpath + "/" + fname

    def get_mask_path(self, fname):
        return os.path.join(PiConf.PHOTO_PATH, fname + "-g.jpg")

    def get_action_pic(self):
        ret = self.last_p_path if self.last_p_path is not None else self.last_s_path
        logging.debug(("Last walk pic", ret, self.last_p_path, self.last_s_path))
        return None if ret is None else ret[len(PiConf.PHOTO_PATH) + 1:-4]


    def draw_action_pic(self,a):
        p_path = os.path.join(PiConf.PHOTO_PATH, self.last_phid + "-p.jpg")
        return self._draw_action_pic(a,p_path)

    def _draw_action_pic(self,a, p_path):
        if not os.path.isfile(self.last_s_path):
            print("No out file")
            return False

        if not os.path.isfile(self.last_g_path):
            print("No mask file")
            return False


        word = "S"
        if a < 0:
            word = "L"
        elif a > 0:
            word = "R"

        rc = wconf.apply_word(self.last_s_path, p_path, word, (0, 0, 255))
        if rc:
            self.last_p_path = p_path
            logging.debug(("Saved action pic", self.last_p_path))
        else:
            print("Cannot draw_action_pic")

        return rc


    def prepare_action(self):
        logging.debug("Prepare walk")
        a = self.get_action()
        if a is None:
            print("No action from pic", self.last_s_path)
            logging.debug(("No action from pic", self.last_s_path))
            self.last_p_path = None
            return False
        logging.debug(("Prepare action", a, self.last_s_path, self.last_g_path))
        rc = self.draw_action_pic(a)
        return rc

    def get_action(self):

        rc, phid, fpath = self.get_photo()
        if not rc:
            logging.debug(("Cannot get a photo for walk"))
            return None
        self.last_phid = phid
        self.rclass.prepare(fpath)
        g_path = self.get_mask_path(phid)
        logging.debug(("Getting action", fpath, g_path, phid))
        rc = self.rclass.classify(fpath, g_path)
        if rc is not None:
            self.last_g_path = g_path
            self.last_s_path = self.rclass.get_out_path()
            print("Classified", rc, self.last_g_path, self.last_s_path)
        return rc 



class WalkCtrl(PreWalkCtrl):

    motor_ctrl = None
    track_id = None
    iter_n = 0
    max_iter = 100


    def __init__(self, motor, photo, rclass = None):
        PreWalkCtrl.__init__(self, photo, rclass)
        self.motor_ctrl = motor

    def init(self):
        self.track_id = self.get_id()
        return self.track_id


    def next(self):
        self.iter_n += 1
        return self.iter_n <= self.max_iter


    def get_id(self):
        return datetime.now().strftime('%d%m%Y%H%M%S')



    def follow(self):
        logging.debug("Start walk following")

        self.motor_ctrl.set_motors("f", "f")   

        try:
            while(self.next()):
                if not self.follow_step(self.iter_n):
                    break
        except Exception as e:
            logging.exception("Cannot do a walk step")
        finally:
            self.motor_ctrl.set_motors("s", "s")

        logging.debug("Done walk following")



    def follow_step(self, i):
        logging.debug(("Follow walk step", i))
        a = self.get_action()
        logging.debug(("Walking action", a))

        if a is None:
            logging.debug(("No action from pic", self.last_s_path, "last action", self.last_action, "attempt", self.step_attempt))
            self.last_p_path = None
            #return False
            # Make right
            a = 1

    
        self.draw_action_pic(a)

        turn_val = 0.15
        straight_run = 0.5

        if a != 0:
            self.turn(a, turn_val)
        else:
            time.sleep(straight_run)
        return True

    def turn(self, r, t):
        turn_cmd = "s0" if r > 0 else "0s"
        ret_cmd = "f0" if r > 0 else "0f"
        turn = "Right" if r > 0 else "Left"
        logging.debug(("Turn", turn, t))
        self.motor_ctrl.set_motors(turn_cmd[0], turn_cmd[1])
        time.sleep(t)
        self.motor_ctrl.set_motors(ret_cmd[0], ret_cmd[1])




def createWalkCtrl(motor_ctrl, photo_ctrl):
    return WalkCtrl(motor_ctrl, photo_ctrl)
            

if __name__ == '__main__':
    motor_ctrl = MotorCtrl.createMotorCtrl()
    photo_ctrl = PhotoCtrl.createPhotoCtrl()

    f = WalkCtrl(motor_ctrl, photo_ctrl)

    f.prepare_action()
    logging.debug("Prepared----------------")

    f.max_iter = 5
    f.follow()

