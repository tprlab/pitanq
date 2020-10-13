# PiTanq
PiTanq is a home tank built with open source hardware and powered by Raspberry Pi. 

Its primary purpose is to help learning AI for vehicles like self-driving, mapping, location.

Also it is a nice toy.

![PiTanq image](https://github.com/tprlab/tprlab.github.io/blob/master/img/other/pitanq.jpg)

## Articles

- [Raspberry Pi Photo-tank-robot](https://medium.com/@const.toporov/raspberry-pi-photo-tank-robot-cf5ca7288adf)
- [Line following robot with OpenCV and contour-based approach](https://medium.com/@const.toporov/line-following-robot-with-opencv-and-contour-based-approach-417b90f2c298)
- [Robot following a walkway with OpenCV and Tensorflow](https://towardsdatascience.com/robot-following-a-walkway-with-opencv-and-tensorflow-a631eb72cb8c)
- [Raspberry Pi robot with GPS](https://medium.com/@const.toporov/raspberry-pi-robot-with-gps-d6f7a9bc10a6)
- [Robot following a walkway using image segmentation](https://towardsdatascience.com/robot-following-a-walkway-using-image-segmentation-272bebd93a83)
- [Robot-tank with Raspberry Pi and Intel Neural Computer Stick 2](https://towardsdatascience.com/robot-tank-with-raspberry-pi-and-intel-neural-computer-stick-2-77263ca7a1c7)

## Hardware
PiTanq is based on an aluminum chassis (the motors are included).

The motors are controlled by L298N bridge.

Raspberry Pi 3 with Raspbian Jessie is a brain.

The tank equiped with 5MP PiCamera.

The camera mounted on pan-and-tilt stand managed by Raspberry via PWM controller.

The power comes from 2x1850 batteries.

Also there is an ultrasonic distance meter.

## Software
Raspbian Jessie runs on the Raspberry. 

Python service (from this repo) controls the whole tank via REST interface.

* GET /ping 
* GET /version 
* GET /name 
* GET /dist  
* POST /update
* POST /fwd/on 
* POST /fwd/off 
* POST /back/on 
* POST /back/off 
* POST /left/on 
* POST /left/off 
* POST /right/on 
* POST /right/off  
* POST /photo/make 
* GET /photo/:phid 
* GET /photo/list  
* POST /cam/up 
* POST /cam/down 
* POST /cam/right 
* POST /cam/left  
* POST /detect/haar/:phid 
* POST /detect/dnn/:phid
* POST /classify/tf/:phid

* POST /motor/:mode
* POST /follow/start
* POST /follow/stop
* POST /follow/prepare
* GET /follow/id
* GET /follow/photo
* GET /photo/track/:track_id/:ph_id 

* POST /walk/start
* POST /walk/stop
* POST /walk/prepare
* GET /walk/photo

* GET /gps
* POST /nav/start
* POST /nav/stop


This service uses AI frameworks:
- Tensoflow (built by [Sam Abrahams](https://github.com/samjabrahams/tensorflow-on-raspberry-pi))
- OpenCV (built by [me](https://github.com/tprlab/pi-opencv))

And third-party driver for PWM controller from [SunFounder](https://github.com/tprlab/pitanq/blob/master/PCA9685_license.txt)

## Phone application
There is an [android application](https://play.google.com/store/apps/details?id=tprlab.com.pitanq) to control the tank.
Whenever I will learn IOS then an Apple app will be available. Not now.

## Tank
More info about the tank at the product [website](https://pitanq.com)
