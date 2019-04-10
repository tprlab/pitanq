import threading
import time
import logging

import MotorCtrl
import PiConf
from GpsNavCtrl import GpsNavCtrl


class MTNavCtrl(GpsNavCtrl):

    T = None
    stop_flag = False


    def start_nav(self, target):
        if self.T is not None:
            logging.debug(("Nav already started", self.target))
            return False
        self.set_target(target)

        self.stop_flag = False
        self.T = threading.Thread(target=self.go_target)
        self.T.start()
        logging.debug(("Started nav thread", target))
        return True


    def stop_nav(self):
        self.stop_flag = True
        if self.T is not None:
            self.T.join()
            self.T = None
        return True

    def go_target(self):
        GpsNavCtrl.go(self, self.target)
        self.T = None
        logging.debug(("Nav", self.target, "finished"))


def createNavCtrl():
    return MTNavCtrl()


if __name__ == '__main__':
    nav = createNavCtrl()

