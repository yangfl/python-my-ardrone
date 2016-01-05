#!/usr/bin/env python
#coding=utf8
from __future__ import absolute_import, print_function

import termios
import traceback
import sys
from time import sleep

from ardrone.interface import ARDrone
from ardrone.script import init


def main():
    fd = sys.stdin.fileno()  # 0, of course.

    oldterm = termios.tcgetattr(fd)
    newterm = termios.tcgetattr(fd)
    newterm[3] = newterm[3] & ~termios.ICANON & ~termios.ECHO
    termios.tcsetattr(fd, termios.TCSANOW, newterm)

    drone = ARDrone()
    init(drone)

    try:
        while True:
            char = sys.stdin.read(1).lower()
            print("Got character", '\\n' if char == '\n' else char)
            eval(char + '()')
    except:
        traceback.print_exc()

    print('landing...')
    l()

    drone.halt()

    termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)


if __name__ == "__main__":
    main()
