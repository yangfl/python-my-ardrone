from time import sleep

from .header import *
from .at import ARDroneAt
from .navdata import ARDroneNavdata

class ARDrone(object):
    def __init__(
            self, ip=ARDRONE_IP, command_port=ARDRONE_COMMAND_PORT,
            navdata_port=ARDRONE_NAVDATA_PORT, video_port=ARDRONE_VIDEO_PORT):
        self.ip = ip
        self.command_port = command_port
        self.navdata_port = navdata_port
        self.video_port = video_port

    def start(self):
        self.navdata = ARDroneNavdata(self.ip, self.navdata_port)
        self.at = ARDroneAt(self.ip, self.command_port)
        self.at("CONFIG", "general:navdata_demo", "TRUE")

    @property
    def takeoffp(self):
        while True:
            navdata = self.navdata()
            if navdata:
                return navdata[0]['drone_state']['fly_mask']
            print('delay navdata')
            sleep(2)

    def takeoff(self, height=None):
        self.trim()
        self.at("REF", True)

    def land(self):
        self.at("REF", False)

    def hover(self):
        self.at("PCMD", False, 0, 0, 0, 0)

    def move(self, lr=0.0, fb=0.0, vv=0.0, va=0.0):
        self.at("PCMD", True, lr, fb, vv, va)

    def move_left(self, speed=1.0):
        self.move(lr=-speed)

    def move_right(self, speed=1.0):
        self.move(lr=speed)

    def move_forward(self, speed=1.0):
        self.move(fb=-speed)

    def move_backward(self, speed=1.0):
        self.move(fb=speed)

    def move_up(self, speed=1.0):
        self.move(vv=speed)

    def move_down(self, speed=1.0):
        self.move(vv=-speed)

    def turn_left(self, speed=1.0):
        self.move(va=-speed)

    def turn_right(self, speed=1.0):
        self.move(va=speed)

    def reset(self):
        self.at("REF", False, True)
        sleep(2)
        self.at("REF", False, False)

    def trim(self):
        self.at("FTRIM")

    def halt(self):
        """Shutdown the drone.

        This method does not land or halt the actual drone, but the
        communication with the drone. You should call it at the end of your
        application to close all sockets, pipes, processes and threads related
        with this object.
        """
        self.navdata.close()
        self.at.stop()
