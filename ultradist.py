import RPi.GPIO as GPIO
import time
import PiConf

 

def init():
    GPIO.setup(PiConf.DIST_TRIGGER, GPIO.OUT)
    GPIO.setup(PiConf.DIST_ECHO, GPIO.IN)

 
def distance():
    # set Trigger to HIGH
    in0 = GPIO.input(PiConf.DIST_ECHO)
    GPIO.output(PiConf.DIST_TRIGGER, GPIO.HIGH)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(PiConf.DIST_TRIGGER, GPIO.LOW)
 
    StartTime = time.time()
    StopTime = time.time()

    ok = False 
    x = -1
    for i in range(1, 1000):
        inp = GPIO.input(PiConf.DIST_ECHO)
        StartTime = time.time()
        if inp == 1:        
            x = i
            ok = True
            break

    if ok == False:
        return -1
    ok = False
    x = -1
 
    for i in range(1, 5000):
        inp = GPIO.input(PiConf.DIST_ECHO)
        StopTime = time.time()
        if inp == 0:
            x = i
            ok = True
            break

    if ok == False:
        return -2

    TimeElapsed = StopTime - StartTime
    distance = (TimeElapsed * 34300) / 2
 
    return distance
 
if __name__ == '__main__':
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    init()

    try:
        for i in range(0,3):
            dist = distance()
            print ("Measured Distance = %.1f cm" % dist)
            time.sleep(1)
 
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()