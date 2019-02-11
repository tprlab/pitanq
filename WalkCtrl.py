import MotorCtrl
import PhotoCtrl
import PiConf

import logging
import time
import numpy as np
import traceback
import math
from datetime import datetime
import os
import walk_conf as wconf
from tf_walk import TFWalkClassifier
import cv2 as cv

MAX_STEP_ATTEMPT = 2

class WalkCtrl:

    motor_ctrl = None
    photo_ctrl = None

    max_iter = 100

    last_act = 0
    last_angle = 0 

    photo_n = 0

    path = None
    g_path = None
    s_path = None
    p_path = None
    last_phid = None

    last_g_path = None
    last_s_path = None
    last_p_path = None

    iter_n = 0

    track_id = None
    last_photo_path = None

    tfc = None

    avg = 0
    prepare = False
    last_action = None
    step_attempt = 0

    def next(self):
        self.iter_n += 1
        return self.iter_n < self.max_iter


    def __init__(self, motor, photo):
        self.motor_ctrl = motor
        self.photo_ctrl = photo

        self.tfc = TFWalkClassifier()
        logging.debug("Initializing TF...")
        self.tfc.init()
        logging.debug("TF inited")
                                                                



    def init(self):
        self.photo_n = 0
        self.iter_n = 0
        self.track_id = self.get_id()
        self.path = PiConf.PHOTO_PATH + "/walk/" + self.track_id
        if not os.path.isdir(self.path):
            os.makedirs(self.path)
        return self.track_id



    def follow(self):
        logging.debug("Start walk following")
        if not self.track_id:
            self.init()

        self.motor_ctrl.set_motors("f", "f")   
        self.last_act = -1

        try:
            while(self.next()):
                if not self.follow_step(self.iter_n):
                    break
        except Exception, e:
            logging.exception("Cannot do a walk step")
        finally:
            self.motor_ctrl.set_motors("s", "s")

        logging.debug("Done walk following")

        self.path = None
        self.track_id = None
        self.photo_n = 0
        self.iter_n = 0


    def follow_step(self, i):
        logging.debug(("Follow walk step", i))
        a = self.get_action()


        if a is None:
            logging.debug(("No action from pic", self.last_s_path, "last action", self.last_action, "attempt", self.step_attempt))
            self.last_p_path = None
            if self.step_attempt > MAX_STEP_ATTEMPT or self.last_action is None:
                return False
            self.step_attempt += 1
            a = self.last_action
        else:
            self.last_action = a
            self.step_attempt = 0

        self.last_action = a
    
        self.draw_action_pic(a)

        turn_val = 0.15
        straight_run = 0.5

        if a != 0:
            self.turn(a, turn_val)
        else:
            time.sleep(straight_run)
        self.last_act = a
        return True



    def get_photo(self):
        logging.debug("Make walk photo")
        rc, phid = self.photo_ctrl.make_photo()
        if rc  == False:
            return False, None, None
        fpath, fname = self.photo_ctrl.get_path(phid)
        if fpath is None:
            return False, None, None
        self.photo_n += 1
        return True, phid, fpath + "/" + fname

    def get_photo_paths(self, fname):
        return PiConf.PHOTO_PATH + "/" + fname  + "-s.jpg", PiConf.PHOTO_PATH + "/" + fname  + "-g.jpg"


    def draw_action_pic(self,a):
        p_path = PiConf.PHOTO_PATH + "/" + self.last_phid + "-p.jpg"
        return self._draw_action_pic(a,p_path)

    def _draw_action_pic(self,a, p_path):
        word = "S"
        if a < 0:
            word = "L"
        elif a > 0:
            word = "R"

        rc = wconf.apply_mask_word(self.last_s_path, self.last_g_path, p_path, (0, 0, 255), word, (255, 0, 0))
        if rc:
            self.last_p_path = p_path
            logging.debug(("Saved action pic", self.last_p_path))

        return rc



    def prepare_action(self):
        self.prepare = True
        logging.debug("Prepare walk")
        a = self.get_action()
        if a is None:
            logging.debug(("No action from pic", self.last_s_path))
            self.last_p_path = None
            return False
        logging.debug(("Prepare action", a, self.last_s_path, self.last_g_path))
        rc = self.draw_action_pic(a)
        self.prepare = False
        self.step_attempt = 0
        self.last_action = None
        return rc

    def get_action_pic(self):
        ret = self.last_p_path if self.last_p_path is not None else self.last_s_path
        logging.debug(("Last walk pic", ret, self.last_p_path, self.last_s_path))
        return None if ret is None else ret[len(PiConf.PHOTO_PATH) + 1:-4]


    def handle_small(self, small, g_path):
        hsv = wconf.to_hsv(small)
        bright = wconf.get_bright(hsv)
        logging.debug(("Saved walk small photo", self.last_s_path, "bright", bright))

        avg = int(bright)
        if self.prepare:
            logging.debug(("Set avg bright", avg))
            self.avg = avg
            ar, ag, ab = wconf.get_avg_rgb(small, 8)
            logging.debug(("Rgb rect", ar, ag, ab))
        else:
            avg = self.avg
            logging.debug(("Use prepared avg", avg))

        gray_EPS = wconf.gray_EPS
        rgb_EPS = wconf.rgb_EPS
        blur = wconf.gray_blur

        gray = wconf.filter_gray(small, gray_EPS, avg, rgb_EPS, blur, g_path)
        self.last_g_path = g_path
        wp = wconf.get_white_percent(gray)
        logging.debug(("Saved walk gray photo", g_path, "avg", avg, "white", wp))
        if wp < wconf.white_threshold:
            logging.debug(("Gray image is all black", wp, avg))
            return None

        #gray = cv.imread(g_path, cv.IMREAD_GRAYSCALE)
        logging.debug(("Classifying", g_path))
        c = self.tfc.classify(gray)
        logging.debug(("Classified as", c))
        if c is None:
            return None
        ret = 0
        if c == TFWalkClassifier.TF_LEFT:
            ret = -1
        if c == TFWalkClassifier.TF_RIGHT:
            ret = 1
        
        return ret


    def get_action(self):

        rc, phid, fpath = self.get_photo()
        if not rc:
            logging.debug(("Cannot get a photo for walk"))
            return None

        #phid = "31012019215149-624507"
        #fpath = PiConf.PHOTO_PATH + "/" + phid + ".jpg"
        self.last_phid = phid

                
        s_path, g_path = self.get_photo_paths(phid)
        
        size = wconf.resize_size
        blur = wconf.resize_blur
        img, small = wconf.blur_resize(fpath, s_path, blur, size)
        if img is None:
            logging.debug(("Cannot load photo", fpath))
            return None

        self.last_s_path = s_path

        return self.handle_small(small, g_path)

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


def createWalkCtrl(motor_ctrl, photo_ctrl):
    return WalkCtrl(motor_ctrl, photo_ctrl)
            

if __name__ == '__main__':

    log_file = "/home/pi/test.log"
    logging.basicConfig(filename=log_file,level=logging.DEBUG, format='%(asctime)s.%(msecs)03d %(threadName)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')


    motor_ctrl = MotorCtrl.createMotorCtrl()
    photo_ctrl = PhotoCtrl.createPhotoCtrl()

    f = WalkCtrl(motor_ctrl, photo_ctrl)
    s_path = "/home/pi/pls.jpg"    
    f.last_s_path = s_path

    img = cv.imread(s_path)
    g_path = "/home/pi/g2.jpg"
    a = f.handle_small(img, g_path)
    #f._draw_action_pic(a, "/home/pi/p2.jpg")
    print "Predict", a