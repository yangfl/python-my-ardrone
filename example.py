#!/usr/bin/env python
#coding=utf8
from __future__ import absolute_import, print_function, division

from ardrone import *
from time import sleep
from math import *

drone = ARDrone()

@use_ardrone(drone)
def mode1():
    for i in range(5):
        r
    h
    for i in range(3):
        f
    h
    for i in range(5):
        l
    h
    for i in range(3):
        b
    h

@use_ardrone(drone)
def mode2():
    for i in range(5):
        r +.5 & f +.866
    h
    for i in range(5):
        r +.5 & b +.866
    h
    for i in range(5):
        l
    h

@use_ardrone(drone)
def mode3():
    for ang in range(0, 360, 15):
        ang = radians(ang)
        s_r = cos(ang)
        s_f = sin(ang)
        r +s_r & b +s_f

@use_ardrone(drone)
def mode4():
    for ang in range(0, 360, 15):
        ang = radians(ang)
        s_r = cos(ang) /4
        s_f = sin(ang) /4
        r +s_r & b +s_f
    h
    for ang in range(360, 0, -15):
        ang = radians(ang)
        s_r = cos(ang) /4
        s_f = sin(ang) /4
        r +s_r & b +s_f
    h

def my_1func(a, ang):
    rad_ang = radians(ang)
    return (2 * cos(rad_ang), sin(rad_ang))

@use_ardrone(drone)
def mode6():
    a = 1
    step = 15
    end = 361

    l_x, l_y = 2, 0
    ang = 0

    while ang < end:
        while True:
            x, y = my_1func(a, ang + step)
            d_x, d_y = x - l_x, y - l_y
            if abs(d_x) < 1 and abs(d_x) < 1:
                ang += step
                l_x, l_y = x, y
                break
            step /= 2
        r +d_x & b +d_y
    h

@use_ardrone(drone)
def recovery():
    z
    y
    z


drone.start()
recovery()

drone.takeoff()


import traceback

while True:
    drone.hover()

    try:            
        mode = input("choose: ")
        if mode == -1:
            break
        globals()['mode'+str(mode)]()
    except KeyboardInterrupt:
        drone.land()
        break
    except:
        traceback.print_exc()

print('landing...')
drone.land()
