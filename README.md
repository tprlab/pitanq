# PiTanq
PiTanq is a home tank built with open source hardware and powered by Raspberry Pi. 

Its primary purpose is to help learning AI for vehicles like self-driving, mapping, location.

Also it is a nice toy.

![PiTanq image](https://github.com/tprlab/tprlab.github.io/blob/master/img/other/pitanq.jpg)

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

This service uses AI frameworks:
- Tensoflow (built by [Sam Abrahams](https://github.com/samjabrahams/tensorflow-on-raspberry-pi))
- OpenCV (built by [me](https://github.com/tprlab/pi-opencv))

And third-party driver for PWM controller from [SunFounder](https://github.com/tprlab/pitanq/blob/master/PCA9685_license.txt)

## Phone application
There is an [android application](https://play.google.com/store/apps/details?id=tprlab.com.pitanq) to control the tank.
Whenever I will learn IOS then an Apple app will be available. Not now.

## Tank
More info about tank at the product [website](https://pitanq.com)
