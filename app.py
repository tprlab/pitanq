from flask import Flask, jsonify, request, send_from_directory
import requests
import logging
import time
import json
import os

import PiConf
import AppCtrl


if not os.path.isdir(PiConf.LOG_PATH):
    os.makedirs(PiConf.LOG_PATH)        

log_file = PiConf.LOG_PATH + "/" + PiConf.LOG_FILE
logging.basicConfig(filename=log_file,level=logging.DEBUG)

app = Flask(__name__)
app_ctrl = AppCtrl.createCtrl()

@app.route('/')
def index():
    return 'Hello world'


@app.route('/ping', methods=['GET'])
def ping():
    return jsonify(app_ctrl.ping()), requests.codes.ok

@app.route('/version', methods=['GET'])
def version():
    return jsonify({"version" : PiConf.VERSION}), requests.codes.ok


@app.route('/name', methods=['GET'])
def name():
    return jsonify(app_ctrl.name()), requests.codes.ok




@app.route('/fwd/on', methods=['POST'])
def forward_on():
    return jsonify(app_ctrl.fwd_on()), requests.codes.ok

@app.route('/fwd/off', methods=['POST'])
def forward_off():
    return jsonify(app_ctrl.fwd_off()), requests.codes.ok

@app.route('/motor/<mode>', methods=['POST'])
def set_motors(mode):
    if len(mode) < 2:
        return jsonify({"rc" : False, "lc" : False}), requests.codes.ok
        
    return jsonify(app_ctrl.set_motors(mode[0], mode[1])), requests.codes.ok



@app.route('/back/on', methods=['POST'])
def backward_on():
    return jsonify(app_ctrl.back_on()), requests.codes.ok

@app.route('/back/off', methods=['POST'])
def backward_off():
    return jsonify(app_ctrl.back_off()), requests.codes.ok


@app.route('/left/on', methods=['POST'])
def left_on():
    return jsonify(app_ctrl.left_on()), requests.codes.ok

@app.route('/left/off', methods=['POST'])
def left_off():
    return jsonify(app_ctrl.left_off()), requests.codes.ok



@app.route('/right/on', methods=['POST'])
def right_on():
    return jsonify(app_ctrl.right_on()), requests.codes.ok

@app.route('/right/off', methods=['POST'])
def right_off():
    return jsonify(app_ctrl.right_off()), requests.codes.ok

@app.route('/photo/make', methods=['POST'])
def make_photo():
    return jsonify(app_ctrl.make_photo()), requests.codes.ok

@app.route('/photo/<phid>', methods=['GET'])
def get_photo(phid):
    path, filename = app_ctrl.getPhotoPath(phid)
    if path is None:
        return "File not found", requests.codes.not_found
    return send_from_directory(directory=path, filename=filename)

@app.route('/photo/list', methods=['GET'])
def get_photos():
    lst = app_ctrl.getPhotosList()
    return jsonify({"list" : lst}), requests.codes.ok


@app.route('/cam/up', methods=['POST'])
def cam_up():
    return jsonify(app_ctrl.cam_up()), requests.codes.ok

@app.route('/cam/down', methods=['POST'])
def cam_down():
    return jsonify(app_ctrl.cam_down()), requests.codes.ok

@app.route('/cam/right', methods=['POST'])
def cam_right():
    return jsonify(app_ctrl.cam_right()), requests.codes.ok

@app.route('/cam/left', methods=['POST'])
def cam_left():
    return jsonify(app_ctrl.cam_left()), requests.codes.ok

@app.route('/detect/haar/<phid>', methods=['POST'])
def detect_haar(phid):
    return jsonify({"rects" : app_ctrl.detect_haar(phid)}), requests.codes.ok

@app.route('/detect/dnn/<phid>', methods=['POST'])
def detect_dnn(phid):
    return jsonify({"rs" : app_ctrl.detect_dnn(phid)}), requests.codes.ok

@app.route('/classify/tf/<phid>', methods=['POST'])
def classify_tf(phid):
    return jsonify({"rs" : app_ctrl.classify(phid)}), requests.codes.ok


@app.route('/update', methods=['POST'])
def update():
    return jsonify(app_ctrl.update()), requests.codes.ok


@app.route('/dist', methods=['GET'])
def dist():
    return jsonify({"rs" : app_ctrl.dist()}), requests.codes.ok


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')