import time
import picamera
from datetime import datetime
import sys
import subprocess

def photo(path):
    subprocess.call(["raspistill", "-t", "1500", "-w", "640", "-h", "480", "-o", path])

def photo_cam(path):
    with picamera.PiCamera() as camera:
        #camera.start_preview()

        #camera.resolution = (2592, 1944)
        #camera.framerate = (1, 1)

        camera.sharpness = 0
        camera.contrast = 0
        camera.brightness = 50
        camera.saturation = 0
        camera.ISO = 0
        camera.video_stabilization = False
        camera.exposure_compensation = 0
        camera.exposure_mode = 'auto'
        camera.meter_mode = 'average'
        camera.awb_mode = 'auto'
        camera.image_effect = 'none'
        camera.color_effects = None
        camera.rotation = 0
        camera.hflip = False
        camera.vflip = False
        camera.crop = (0.0, 0.0, 1.0, 1.0)

        camera.capture(path)

        #camera.stop_preview()

if __name__ == '__main__':    
    fname = None
    if len(sys.argv) > 1:
        fname = sys.argv[1]
    if fname is None:
        tmt = datetime.now().strftime('%d%m%Y-%H%M%S')
        fname = "img/" + tmt + ".jpg"

    time.sleep(0.5)
    photo(fname)
    print ("Saved photo", fname)
        


