import walk_conf as wconf
import PiConf
import PhotoCtrl
import logging
import segment
import segment_ncs
import cv2
import os.path
import sys

class RoadMask:

    gray_path = None
    pic_path = None
    img = None
    pic = None

    def init(self):
        pass

    def handle_pic(self, fpath, mask_path):
        pass

    def prepare(self, fpath):
        pass

    def get_out_path(self):
        pass




class CvRoadMask(RoadMask):

    avg = None
    small_path = None
    out_path = None

    def gen_small_path(self, fpath):
        path, file = os.path.split(fpath)
        print(path, file)
        smfile = "cv-sm-" + file
        return os.path.join(path, smfile)

    def gen_out_path(self, fpath):
        path, file = os.path.split(fpath)
        print(path, file)
        smfile = "cv-out-" + file
        return os.path.join(path, smfile)




    def prepare(self, fpath):
        self.pic_path = fpath
        size = wconf.resize_size
        blur = wconf.resize_blur
        small_path = self.gen_small_path(fpath)

        self.img, self.pic = wconf.blur_resize(fpath, small_path, blur, size)
        if self.img is None:
            logging.debug(("Cannot load photo", fpath))
            return False
        self.small_path = small_path
        return True


    def calibrate(self):
        hsv = wconf.to_hsv(self.pic)
        bright = wconf.get_bright(hsv)

        logging.debug(("Saved walk small photo", self.small_path, "bright", bright))
        avg = int(bright * 1.1)
        logging.debug(("Set avg bright", avg))
        self.avg = avg
        #ar, ag, ab = wconf.get_avg_rgb(self.pic, 8)
        #logging.debug(("Rgb rect", ar, ag, ab))

    def handle_pic(self, fpath, gray_path):
        if not self.prepare(fpath):
            return None
        if self.avg is None:
            self.calibrate()
        return self._handle_pic(gray_path)

    def check_white(self, name, pic):
        wp = wconf.get_white_percent(gray)
        logging.debug(("White balance", name, wp, wconf.white_threshold))
        return wp >= wconf.white_threshold


    def _handle_pic(self, gray_path):
        avg = self.avg
        logging.debug(("Use prepared avg", avg))

        gray_EPS = wconf.gray_EPS
        rgb_EPS = wconf.rgb_EPS
        blur = wconf.gray_blur

        gray = wconf.filter_gray(self.pic, gray_EPS, avg, rgb_EPS, blur, gray_path)
        logging.debug(("Saved walk gray photo", gray_path, "avg", avg))
        wp = wconf.get_white_percent(gray)
        if not self.check_white(gray, gray_path):
            logging.debug("Gray image is all black")
            return None
        self.out_path = self.gen_out_path(self.pic_path)
        wconf.apply_mask(self.small_path, gray_path, self.out_path, (0, 0, 255))
        return gray

    def get_out_path(self):
        return self.out_path


class SegRoadMask(RoadMask):

    net = None
    cls = None
    clr = None

    def init(self):
        self.net, self.cls, self.clr = segment.load_segment_model()
        return self.net is not None

    def gen_out_path(self, fpath):
        path, file = os.path.split(fpath)
        print(path, file)
        smfile = "seg-out-" + file
        return os.path.join(path, smfile)


    def handle_pic(self, fpath, gray_path):
        out, mask = segment.segment_image(fpath, self.net, self.cls, self.clr)
        
        cv2.imwrite(gray_path, mask)
        out_path = self.gen_out_path(fpath)
        cv2.imwrite(out_path, out)
        self.out_path = out_path

        return mask

    def get_out_path(self):
        return self.out_path

class SegNcsRoadMask(RoadMask):

    net = None
    model = None

    def init(self):
        self.model, self.net = segment_ncs.load_segment_model()
        return self.net is not None

    def gen_out_path(self, fpath):
        path, file = os.path.split(fpath)
        print(path, file)
        smfile = "seg-out-ncs-" + file
        return os.path.join(path, smfile)


    def handle_pic(self, fpath, gray_path):
        out, mask = segment_ncs.segment_image(fpath, self.model, self.net)

        out_path = self.gen_out_path(fpath)
        self.out_path = out_path

        cv2.imwrite(out_path, out)
        cv2.imwrite(gray_path, mask)
        return mask

    def get_out_path(self):
        return self.out_path





def createSegRoadMask():
    return SegRoadMask()

def createNcsRoadMask():
    return SegNcsRoadMask()



def testSegMask():
    rmask = createSegRoadMask()
    rmask.init()

    path = "test/data/road.jpg"
    gray_path = "test/data/road-sg.jpg"
    mask = rmask.handle_pic(path, gray_path)

def testNcsMask():
    rmask = createNcsRoadMask()
    rmask.init()

    path = "test/data/road.jpg"
    gray_path = "test/data/road-sg.jpg"
    mask = rmask.handle_pic(path, gray_path)


def createCvRoadMask():
    return CvRoadMask()


def createRoadMask(name = None):
    if name == "cv":
        return createCvRoadMask()
    if name == "seg":
        return createSegRoadMask()
    if name == "ncs":
        return createNcsRoadMask()

    return createNcsRoadMask()


def testCvMask():
    rmask = createCvRoadMask()
    path = "test/data/road.jpg"
    #small_path = "test/data/road-sm.jpg"
    gray_path = "test/data/road-g.jpg"
    rmask.prepare(path)
    rmask.calibrate()
    mask = rmask.handle_pic(path, gray_path)

if __name__ == '__main__':

    #log_file = "/home/pi/road_test.log"
    #logging.basicConfig(filename=log_file,level=logging.DEBUG, format='%(asctime)s.%(msecs)03d %(threadName)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    #testCvMask()
    #testSegMask()
    testNcsMask()

