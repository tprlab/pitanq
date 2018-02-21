import motor
import cam
import os
import time
 


PH_PATH = "photos"

if not os.path.exists(PH_PATH):
    os.makedirs(PH_PATH)

T = 0
t = 0.5


for i in xrange(16):
    fname = PH_PATH + "/photo_" + str(T) + ".jpg"
    time.sleep(1)
    cam.photo(fname)
    T += t
    motor.right(t)
    print i
    
