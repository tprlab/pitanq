import unittest
import requests
import time
import tanq_rest as tanq


class TanqTest(unittest.TestCase):

    def base_call(self, proc, field):
        resp, code = proc()
        self.assertTrue(code, requests.codes.ok)
        self.assertTrue(field in resp, True)

    def print_resp(self, proc):
        resp, code = proc()
        print resp




    def test_ping(self):
        self.base_call(tanq.ping, "rc")

    def test_version(self):
        self.base_call(tanq.version, "version")

    def test_dist(self):
        self.base_call(tanq.dist, "rs")

    def test_name(self):
        self.base_call(tanq.device_name, "name")

    def test_fwd(self):
        self.base_call(tanq.fwd_on, "rc")
        time.sleep(1)
        self.base_call(tanq.fwd_off, "rc")

    def test_back(self):
        self.base_call(tanq.back_on, "rc")
        time.sleep(1)
        self.base_call(tanq.back_off, "rc")

    def test_right(self):
        self.base_call(tanq.right_on, "rc")
        time.sleep(1)
        self.base_call(tanq.right_off, "rc")

    def test_left(self):
        self.base_call(tanq.left_on, "rc")
        time.sleep(1)
        self.base_call(tanq.left_off, "rc")

    def test_camup(self):
        self.base_call(tanq.cam_up, "rc")

    def test_camdown(self):
        self.base_call(tanq.cam_down, "rc")


    def test_camleft(self):
        self.base_call(tanq.cam_left, "rc")

    def test_camright(self):
        self.base_call(tanq.cam_right, "rc")

    def test_make_photo(self):
        self.base_call(tanq.photo, "rc")

    def test_photo_list(self):
        resp, code = tanq.photo_list()
        self.assertTrue(code, requests.codes.ok)
        self.assertFalse(resp is None, True)









        

if __name__ == '__main__':
    unittest.main()
