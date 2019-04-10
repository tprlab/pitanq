from gpss import gpss
import logging
import PiConf
import threading
import subprocess
import time


class GpsCtrl:

    logger = None
    G = None
    version = None
    devices = None
    sats = None
    T = None
    

    def init_gps(self):
        self.G = gpss()
        for i in range(0,5):
            r = self.get_state()
            self.logger.debug(("Gps-init", i, r))
            if r is None:
                continue
            if "class" not in r:
                continue
            c = r["class"]
            if c == "VERSION":
                self.version = r
            elif c == "SKY":
                self.sats = r
            elif c == "DEVICES":
                self.devices = r
            elif c == "TPV":
                return True
        return False

    def init_logger(self):
        log_file = PiConf.LOG_PATH + "/gps.log"
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

        handler = logging.FileHandler(log_file)             
        handler.setFormatter(formatter)

        logger = logging.getLogger("gps")
        logger.setLevel(logging.DEBUG)
        logger.addHandler(handler)
        self.logger = logger

    def __init__(self):
        self.init_logger()
        rc = self.init_gps()
        logging.debug(("Gps inited", rc))
        #self.T = threading.Thread(target=self.gps_timer)
        #self.T.start()


    def get_state(self):
        return self.G.getRaw()

    def gps_timer(self):
        self.logger.debug("Started gps timer")
        cnt = 0
        while cnt < 10000:
            cnt += 1
            info = self.get_state()
            if info is None:
                continue
            if not hasattr(info, "lat"):
                continue
            self.logger.debug(("GpsTimer:", info))
            time.sleep(2)

    
    def get_coords(self):
        for i in range(0,5):
            s = self.get_state()
            #self.logger.debug(("GPS attempt",i, s))
            if hasattr(s, "lat"):
                ret = {"lat" : s["lat"], "lon" : s["lon"]}
                if hasattr(s, "track"):
                    ret["track"] = s["track"]
                if hasattr(s, "alt"):
                    ret["alt"] = s["alt"]
                if hasattr(s, "speed"):
                    ret["speed"] = s["speed"]

                return ret
            
        return None
        

class MockGps:

    point = None

    def setPoint(self, pt):
        self.point = pt

    def get_coords(self):
        return self.point

def createMockGpsCtrl():
    return MockGps()

def createGpsCtrl():
    return GpsCtrl()

if __name__ == '__main__': 
    log_file = "/home/pi/gps_test.log"
    logging.basicConfig(filename=log_file,level=logging.DEBUG, format='%(asctime)s.%(msecs)03d %(threadName)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    g = createGpsCtrl()

    n = 0
    for i in range(0,10):
        print (i)
        pt = g.get_coords()
        if pt is not None:
            n += 1
            print (pt)
        else:
            time.sleep(1)
        if n > 10:
            break
