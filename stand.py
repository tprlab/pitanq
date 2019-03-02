import PCA9685
import os, os.path
import cam
from datetime import datetime
import logging
import time
import traceback




servo_min = 150 
servo_max = 600


PAN_0 = 450
TILT_0 = 340

class StandCtrl:

    pwm = None
    pan_ch = 1
    tilt_ch = 0
    pan = PAN_0
    tilt = TILT_0
    pan_step = 30
    tilt_step = 30

    def __init__(self):
        try:
            self.pwm = PCA9685.PWM()
            self.pwm.frequency = 60
            self.pwm.write(self.pan_ch, 0, self.pan)
            self.pwm.write(self.tilt_ch, 0, self.tilt)    
        except:
            logging.debug("PWM disabled")


    def down(self):
        if self.pwm is None:
            return False
        if self.pan < servo_max:
            self.pan += self.pan_step
            self.pwm.write(self.pan_ch, 0, self.pan)
            return True
        return False
        

    def up(self):
        if self.pwm is None:
            return False

        if self.pan > servo_min:
            self.pan -= self.pan_step
            self.pwm.write(self.pan_ch, 0, self.pan)
            return True
        return False



    def left(self):
        if self.pwm is None:
            return False

        if self.tilt < servo_max:
            self.tilt += self.tilt_step
            self.pwm.write(self.tilt_ch, 0, self.tilt)
            return True
        return False

    def right(self):
        if self.pwm is None:
            return False

        if self.tilt > servo_min:
            self.tilt -= self.tilt_step
            self.pwm.write(self.tilt_ch, 0, self.tilt)
            return True
        return False


  


def createStandCtrl():
    return StandCtrl()

if __name__ == '__main__':    
    stand = StandCtrl()
    print ("Pan+")
    stand.up()
    time.sleep(1)
    print ("Tilt+")
    stand.right()

    time.sleep(1)
    print ("Pan-")
    stand.down()

    time.sleep(1)
    print ("Tilt-")
    stand.left()

