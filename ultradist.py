#Libraries
import RPi.GPIO as GPIO
import time
 
#GPIO Mode (BOARD / BCM)
#GPIO.setmode(GPIO.BCM)

 
#set GPIO Pins
GPIO_TRIGGER = 37
GPIO_ECHO = 35
#set GPIO direction (IN / OUT)

def init():
    GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
    GPIO.setup(GPIO_ECHO, GPIO.IN)

 
def distance():
    # set Trigger to HIGH
    in0 = GPIO.input(GPIO_ECHO)
    GPIO.output(GPIO_TRIGGER, GPIO.HIGH)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, GPIO.LOW)
 
    StartTime = time.time()
    StopTime = time.time()

    ok = False 
    x = -1
    # save StartTime
    for i in range(1, 1000):
        inp = GPIO.input(GPIO_ECHO)
        StartTime = time.time()
        if inp == 1:        
            x = i
            ok = True
            break

    if ok == False:
        return -1
    #print x

    ok = False
    x = -1
 
    # save time of arrival
    for i in range(1, 100000):
        inp = GPIO.input(GPIO_ECHO)
        StopTime = time.time()
        if inp == 0:
            x = i
            ok = True
            break

    if ok == False:
        return -2

    #print x
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance
 
if __name__ == '__main__':
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)        # Number GPIOs by its physical location
    init()

    try:
        for i in range(0,3):
            dist = distance()
            print ("Measured Distance = %.1f cm" % dist)
            time.sleep(1)
 
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()