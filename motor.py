import RPi.GPIO as GPIO
import time
import logging

 

RF = 40
RB = 38

LF = 36
LB = 32

motors = [RF, RB, LF, LB]

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
    

def run_motor(m, t):
    GPIO.output(m,GPIO.HIGH)
    time.sleep(t)
    GPIO.output(m,GPIO.LOW)

 



def forward(t):
    GPIO.output(RF, GPIO.HIGH)
    GPIO.output(LF, GPIO.HIGH)
    time.sleep(t)
    GPIO.output(RF, GPIO.LOW)
    GPIO.output(LF, GPIO.LOW)

def back(t):
    logging.debug("Motor back for %f sec" % t)
    GPIO.output(RB, GPIO.HIGH)
    GPIO.output(LB, GPIO.HIGH)
    time.sleep(t)
    GPIO.output(RB, GPIO.LOW)
    GPIO.output(LB, GPIO.LOW)

def right(t):
    GPIO.output(RF, GPIO.HIGH)
    GPIO.output(LB, GPIO.HIGH)
    time.sleep(t)
    GPIO.output(RF, GPIO.LOW)
    GPIO.output(LB, GPIO.LOW)

def left(t):
    GPIO.output(LF, GPIO.HIGH)
    GPIO.output(RB, GPIO.HIGH)
    time.sleep(t)
    GPIO.output(LF, GPIO.LOW)
    GPIO.output(RB, GPIO.LOW)


def fwd_on():
    logging.debug("Motor fwd on")    
    GPIO.output(RF, GPIO.HIGH)
    GPIO.output(LF, GPIO.HIGH)

def fwd_off():
    logging.debug("Motor fwd off")    
    GPIO.output(RF, GPIO.LOW)
    GPIO.output(LF, GPIO.LOW)


def back_on():
    logging.debug("Motor back on")
    GPIO.output(RB, GPIO.HIGH)
    GPIO.output(LB, GPIO.HIGH)

def back_off():
    logging.debug("Motor back off")
    GPIO.output(RB, GPIO.LOW)
    GPIO.output(LB, GPIO.LOW)


def right_on():
    logging.debug("Motor right on")
    GPIO.output(RF, GPIO.HIGH)
    GPIO.output(LB, GPIO.HIGH)

def right_off():
    logging.debug("Motor right off")
    GPIO.output(RF, GPIO.LOW)
    GPIO.output(LB, GPIO.LOW)

def left_on():
    logging.debug("Motor left on")
    GPIO.output(LF, GPIO.HIGH)
    GPIO.output(RB, GPIO.HIGH)


def left_off():
    logging.debug("Motor left off")
    GPIO.output(LF, GPIO.LOW)
    GPIO.output(RB, GPIO.LOW)


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
    #forward(2)
    #right(2)
    #back(2)
    #right(3)
    #left(2)
    #stop()

    #back_test(2)
    fwd_test(2)
    
     
    #GPIO.cleanup()