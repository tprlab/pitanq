import GpsCtrl
import logging
import PiConf
import time
import math
import MotorCtrl
import GpsUtil



class GpsNavCtrl:

    gps = None
    drive = None
    target = None
    pos = None
    az = None
    TURN_HALF = 1
    
    MAX_ITERATIONS = 10
    DIST_EPS = 0.003
    STEP_LEN = 5
    AZ_LEN = 3
    ANGLE_EPS = 0.001
    
    

    def init(self, g, d):
        self.gps = g
        self.drive = d
        

    def set_target(self, pt):
        self.target = pt


    def findAzimuth(self, t):
        pos0 = self.gps.get_coords()
        if pos0 is None:
            logging.debug("Gps not ready to get azimuth")
            return None
        self.drive.fwd_on()
        time.sleep(t)
        self.drive.fwd_off()
        pos1 = self.gps.get_coords()
        if pos1 is None:
            logging.debug("Gps not ready to find azimuth")
            return None

        az = GpsUtil.azimuth(pos0, pos1)
        logging.debug(("Azimuth of", pos0, "to", pos1, "is", az))
        return az        

    def turn(self, a):
        td = 1 if a > 0 else 0
        aa = abs(a)
        tt = self.TURN_HALF * aa / 6.28
        logging.debug(("Turning for", tt, td, "to direct", a))
        on = self.drive.right_on if td > 0 else self.drive.left_on
        off = self.drive.right_off if td > 0 else self.drive.left_off
        on()
        time.sleep(tt)
        off()

    def forward(self, t):
        self.drive.fwd_on()
        time.sleep(t)
        self.drive.fwd_off()


    def go_step(self, t, target, pos):
        d = GpsUtil.gps_dist(pos, target)
        logging.debug(("Going to target", target, "from", pos, "distance", d))

        taz = GpsUtil.azimuth(pos, target)
        logging.debug(("Target azimuth", taz, "local", self.az))

        daz = taz - self.az
        if abs(daz) > self.ANGLE_EPS:
            self.turn(daz)
            self.az = taz

        self.forward(t)

        pos1 = self.gps.get_coords()
        if pos1 is None:
            logging.debug(("Cannot finish go iteration", target))
            return None, None

        track = pos1["track"] if "track" in pos1 else None
        laz = GpsUtil.azimuth(pos, pos1)
        logging.debug(("Updated direction",track, laz, self.az))

        if track is not None and abs(track) > self.ANGLE_EPS:
            rt = GpsUtil.toRadians2(track)
            self.az = rt
        else:
            self.az = laz



        d = GpsUtil.gps_dist(pos1, target)
        logging.debug(("Going to target step", target, "from", pos1, "distance", d))        
        return pos1, d


    def go(self, target):
        if target is None:
            return False, None, None
        try:
            logging.debug(("Go to target", target))
            if self.az is None:
                az = self.findAzimuth(self.AZ_LEN)
                logging.debug(("Found initial azimuth", az))
                if az is None:
                    return None, None,None
                self.az = az

            pos = self.gps.get_coords()
            if pos is None:
                logging.debug(("Gps not ready to go to target ", target))
                return None, None, None
            d= GpsUtil.gps_dist(pos, target)
            logging.debug(("Initial distance", d, pos))
            success = False
            for i in range(0, self.MAX_ITERATIONS):
                pos, d = self.go_step(self.STEP_LEN, target, pos)
                logging.debug(("Go moved to ", i, pos, d))
                if pos is None:
                    logging.debug("Go stopped because no pos")
                    break
                if d < self.DIST_EPS:
                    logging.debug(("Target is reached", d, pos))
                    break

            logging.debug(("Final distance", d, pos, success))
            return success, pos, d
        except:
            logging.exception("Cannot go nav")
        return False, None, None
       

def createGpsNavCtrl():
    return GpsNavCtrl()

class MockGps:
    lat1 = GpsUtil.nyc_lat
    lon1 = GpsUtil.nyc_lon

    lats = {}
    lons = {}

    num = 0
    mode = None

    def __init__(self, mode):
        self.lats["n"] = GpsUtil.mont_lat
        self.lons["n"] = GpsUtil.mont_lon


        self.lats["e"] = GpsUtil.frg_lat
        self.lons["e"] = GpsUtil.frg_lon

        self.lats["s"] = GpsUtil.sh_lat
        self.lons["s"] = GpsUtil.sh_lon

        self.lats["w"] = GpsUtil.newark_lat
        self.lons["w"] = GpsUtil.newark_lon

        self.mode = mode
    
    def get_coords(self):
        if self.num == 0:
            self.num += 1
            return {"lat" : self.lat1, "lon" : self.lon1}
        elif self.num == 1:
            self.num += 1
            return {"lat" : self.lats[self.mode], "lon" : self.lons[self.mode]}
        return None

class MockDrive:
    def fwd_on(self):
        return True

    def fwd_off(self):
        return True




if __name__ == '__main__': 

    log_file = "/home/pi/gps_nav_test.log"
    logging.basicConfig(filename=log_file,level=logging.DEBUG, format='%(asctime)s.%(msecs)03d %(threadName)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    target = GpsUtil.nyc_pos
                
    nav = createGpsNavCtrl()
    gps = GpsCtrl.createGpsCtrl()
    drive = MotorCtrl.createMotorCtrl()
    nav.init(gps, drive)

    pt = None
    for i in range(0,5):
        pt = gps.get_coords()
        if pt is not None:
            break
    if pt is not None:
        logging.debug(("Got initial position", pt))
        rc, pos, dist = nav.go(target)
        print ("Go results", rc, pos, dist)
    
    """

    mgps = MockGps("n")
    md = MockDrive()
    nav.init(mgps, md)
    """
