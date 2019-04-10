import requests
import time
import json
import sys
import os


URL = "http://192.168.1.164:5000"
    
def tanq_post(path, params = None):
    headers = {'Content-type': 'application/json'}
    rsp = requests.post(URL + path, data=json.dumps(params), headers=headers)
    #print path, rsp.status_code, rsp.content
    ret = rsp.json() if rsp.status_code == requests.codes.ok else rsp.content
    return ret, rsp.status_code

def tanq_get(path):
    rsp = requests.get(URL + path)
    print path, rsp.status_code, rsp.content
    ret = rsp.json() if rsp.status_code == requests.codes.ok else rsp.content
    return ret, rsp.status_code


def fwd_on():
    return tanq_post("/fwd/on")

def fwd_off():
    return tanq_post("/fwd/off")

def back_on():
    return tanq_post("/back/on")

def back_off():
    return tanq_post("/back/off")

def right_on():
    return tanq_post("/right/on")

def right_off():
    return tanq_post("/right/off")

def left_on():
    return tanq_post("/left/on")

def left_off():
    return tanq_post("/left/off")

def set_motors(mode):
    return tanq_post("/motor/" + mode)



def photo():
    return tanq_post("/photo/make")

def photo_list():
    js, code = tanq_get("/photo/list")
    ret = None if code != requests.codes.ok else js["list"]
    return ret, code

def device_name():
    return tanq_get("/name")

def cam_up():
    return tanq_post("/cam/up")

def cam_down():
    return tanq_post("/cam/down")

def cam_left():
    return tanq_post("/cam/left")


def cam_right():
    return tanq_post("/cam/right")

def detect_haar(id):
    return tanq_post("/detect/haar/" + id)

def detect_dnn(id):
    return tanq_post("/detect/dnn/" + id)


def version():
    return tanq_get("/version")

def ping():
    return tanq_get("/ping")

def dist():
    return tanq_get("/dist")

def classify_tf(id):
    return tanq_post("/classify/tf/" + id)

def start_follow():
    return tanq_post("/follow/start")

def prepare_follow():
    return tanq_post("/follow/prepare")

def stop_follow():
    return tanq_post("/follow/stop")

def follow_id():
    resp, rc = tanq_get("/follow/id")
    return resp

def follow_photo():
    resp, rc = tanq_get("/follow/photo")
    return resp

def prepare_path():
    return tanq_post("/path/prepare")


def get_gps():
    return tanq_get("/gps")

def start_nav():
    return tanq_post("/nav/start", params={"lat":40.1, "lon" : -74.1})


def get_photo(pid, outpath = "./"):
    path = "/photo/" + pid
    rsp = requests.get(URL + path, stream=True)
    if rsp.status_code != requests.codes.ok:
        print("No photo %s found" % pid)
        return

    fname = outpath + "/" + pid + ".jpg"
    slash = fname.rfind("/")
    folder = fname[:slash]
    print "Folder", folder
    if not os.path.exists(folder):
        os.makedirs(folder)

    with open(fname, "wb") as f:
        for chunk in rsp.iter_content(1024):
            f.write(chunk)

    print ("Saved", fname)
    return fname

def test_follow_prepare():
    r = prepare_follow()
    print r
    r = follow_photo()
    print r
    ph = r["photo"]
    get_photo(ph)
   

def test_path_prepare():
    rs, rc = prepare_path()
    if rc == requests.codes.ok:
        get_photo(rs["path"])
    else:
        print rc, rs
 

def test_follow():
    start_follow()
    fid = follow_id()
    print "Started follow", fid

    for i in xrange(0, 10):
        time.sleep(0.5)
        pr = follow_photo()
        print "Follow photo", pr
        if pr["photo"] is not None:
            get_photo(pr["photo"])
    stop_follow()


if __name__ == '__main__':
    #print classify_tf(sys.argv[1])
    #print device_name()
    """
    set_motors("ff")
    time.sleep(2)
    print("stop left")
    set_motors("0s")
    time.sleep(0.1)
    set_motors("0f")
    time.sleep(2)
    print("stop all")
    set_motors("ss")
    """
    #test_follow_prepare()

    #rs, rc = get_path_color_range()
    #print rs, rc

    #rs, rc = set_path_color_range([26, 121,  59], [27, 225, 122], "hsv")

    #rs, rc = set_path_color_range([24, 120,  64], [25, 207,  96], "hsv")
    #rs, rc = set_path_color_range([23, 101, 53], [28, 221, 116], "hsv")

    #rs, rc = set_path_color_range([53, 42, 7], [116, 113, 70], "rgb")
    #print rc
    #rs, rc = get_path_color_range()
    #print rs, rc
    #test_path_prepare()
    ret, code = get_gps()
    print code, ret

    ret, code = start_nav()
    print code, ret

