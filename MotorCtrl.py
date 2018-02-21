import motor
import logging


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




def createMotorCtrl():
    return MotorCtrl()



