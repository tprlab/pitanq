import motor
import logging
import time


class MotorCtrl:

    def __init__(self):
        motor.init()


    def safeMotorCall(self, proc, opname):
        try:
            proc()
            return True
        except:
            logging.exception(opname)
        return False
            

    def fwd_on(self):
        return self.safeMotorCall(motor.fwd_on, "motor.fwd_on")

    def fwd_off(self):
        return self.safeMotorCall(motor.fwd_off, "motor.fwd_off")

    def back_on(self):
        return self.safeMotorCall(motor.back_on, "motor.back_on")

    def back_off(self):
        return self.safeMotorCall(motor.back_off, "motor.back_off")

    def right_on(self):
        return self.safeMotorCall(motor.right_on, "motor.right_on")

    def right_off(self):
        return self.safeMotorCall(motor.right_off, "motor.right_off")

    def left_on(self):
        return self.safeMotorCall(motor.left_on, "motor.left_on")

    def left_off(self):
        return self.safeMotorCall(motor.left_off, "motor.left_off")

    def set_motors(self, r, l):
        lc = False
        rc = False
        logging.debug("Set motors " + r + " " + l)
        if r == "f":
            rc = self.safeMotorCall(motor.motor_right_on, "motor.motor_right_on")
        elif r == "s":
            rc = self.safeMotorCall(motor.motor_right_off, "motor.motor_right_off")
        elif r == "r":
            rc = self.safeMotorCall(motor.motor_rright_on, "motor.motor_rright_on")
        elif r == "h":
            rc = self.safeMotorCall(motor.motor_rright_off, "motor.motor_rright_off")


        if l == "f":
            lc = self.safeMotorCall(motor.motor_left_on, "motor.motor_left_on")
        elif l == "s":
            lc = self.safeMotorCall(motor.motor_left_off, "motor.motor_left_off")
        elif l == "r":
            rc = self.safeMotorCall(motor.motor_rleft_on, "motor.motor_rleft_on")
        elif l == "h":
            rc = self.safeMotorCall(motor.motor_rleft_off, "motor.motor_rleft_off")

        return rc, lc






def createMotorCtrl():
    return MotorCtrl()


if __name__ == '__main__': 
    m = createMotorCtrl()
    t = 2.5
    m.right_on()
    time.sleep(t)
    m.right_off()

