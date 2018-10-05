import RPi.GPIO as GPIO
import time
import logging
import PiConf

 

LF = PiConf.MOTOR_LF
LB = PiConf.MOTOR_LB

RF = PiConf.MOTOR_RF
RB = PiConf.MOTOR_RB

motors = [RF, RB, LF, LB]

R_state = 0
L_state = 0

def init():

    logging.debug("Motor init")
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    GPIO.cleanup() 


    for m in motors:
        GPIO.setup(m,GPIO.OUT)
        GPIO.setup(m,GPIO.LOW)

def stop():
    logging.debug("Motor stop")
    for m in motors:
        GPIO.setup(m,GPIO.LOW)

# Motor    

def run_motor(m, t):
    GPIO.output(m,GPIO.HIGH)
    time.sleep(t)
    GPIO.output(m,GPIO.LOW)

# Motor forward

def motor_right_on():
    logging.debug("Motor right on")
    GPIO.output(RF, GPIO.HIGH)

def motor_right_off():
    logging.debug("Motor right off")
    GPIO.output(RF, GPIO.LOW)

def motor_left_on():
    logging.debug("Motor left on")
    GPIO.output(LF, GPIO.HIGH)

def motor_left_off():
    logging.debug("Motor left off")
    GPIO.output(LF, GPIO.LOW)

# Motor reverse

def motor_rright_on():
    logging.debug("Motor rright on")
    GPIO.output(RB, GPIO.HIGH)

def motor_rright_off():
    logging.debug("Motor rright off")
    GPIO.output(RB, GPIO.LOW)

def motor_rleft_on():
    logging.debug("Motor rleft on")
    GPIO.output(LB, GPIO.HIGH)


def motor_rleft_off():
    logging.debug("Motor rleft off")
    GPIO.output(LB, GPIO.LOW)
 
## Turns

#Left

def turn_left_on():
    logging.debug("Turn left on")
    motor_right_on()

def turn_left_off():
    logging.debug("Turn left off")
    motor_right_off()

def turn_xleft_on():
    logging.debug("Turn xleft on")
    motor_right_on()
    motor_rleft_on()

def turn_xleft_off():
    logging.debug("Turn xleft off")
    motor_right_off()
    motor_rleft_off()

# Right

def turn_right_on():
    logging.debug("Turn right on")
    motor_left_on()

def turn_right_off():
    logging.debug("Turn right off")
    motor_left_off()

def turn_xright_on():
    logging.debug("Turn xright on")
    motor_left_on()
    motor_rright_on()

def turn_xright_off():
    logging.debug("Turn xright off")
    motor_left_off()
    motor_rright_off()


## Test

def forward(t):
    motor_right_on()
    motor_left_on()
    time.sleep(t)
    motor_right_off()
    motor_left_off()

def back(t):
    motor_rright_on()
    motor_rleft_on()
    time.sleep(t)
    motor_rright_off()
    motor_rleft_off()

def right(t):
    turn_xright_on()
    time.sleep(t)
    turn_xright_off()

def left(t):
    turn_xleft_on()
    time.sleep(t)
    turn_xleft_off()

# API

def fwd_on():
    logging.debug("fwd on")    
    motor_right_on()
    motor_left_on()

def fwd_off():
    logging.debug("fwd off")    
    motor_right_off()
    motor_left_off()


def back_on():
    logging.debug("back on")
    motor_rright_on()
    motor_rleft_on()

def back_off():
    logging.debug("back off")
    motor_rright_off()
    motor_rleft_off()


def right_on():
    turn_right_on()

def right_off():
    turn_right_off()

def left_on():
    turn_left_on()

def left_off():
    turn_left_off()



def back_test(t):
    back_on()
    time.sleep(t)
    back_off()

def fwd_test(t):
    fwd_on()
    time.sleep(t)
    fwd_off()

        

if __name__ == '__main__':    
    init()
    #run_motor(LB, 2) 
    forward(2)
    #right(2)
    #back(2)
    #right(3)
    #left(2)
    #stop()
    #fwd_off()

    #back_test(2)
    #fwd_test(2)
    
     
    #GPIO.cleanup()