from __future__ import print_function

from .header import *
from .command import translator
from funcutils import Namespace

import socket
import threading


class ARDroneAt:
    def __init__(self, ip=ARDRONE_IP, port=ARDRONE_COMMAND_PORT):
        self.comwdg_interval = COMWDG_INTERVAL
        self.address = (ip, port)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.cv = threading.Condition()
        self.thread = Namespace(is_alive=lambda: False)
        self.start()

    def start(self):
        if not self.thread.is_alive():
            self.thread = threading.Thread(target=self.loop)
            self.thread.daemon = True
            self.stopped = False
            self.monad_command = translator()
            self.thread.start()

    def stop(self):
        self.stopped = True
        self.cv.notify()

    def loop(self):
        with self.cv:
            while True:
                self.cv.wait(self.comwdg_interval)
                if self.stopped:
                    break
                self.monad_command, msg = self.monad_command()
                if DEBUG and not msg.startswith('AT*COMWDG'):
                    print(msg[:-1].replace('\r', '\n'))
                self.s.sendto(msg, self.address)
                self.cv.notify()

    def push(self, cmd, *args, **kwargs):
        with self.cv:
            self.monad_command = self.monad_command(cmd, *args, **kwargs)

    def send(self, cmd, *args, **kwargs):
        with self.cv:
            self.push(cmd, *args, **kwargs)
            self.cv.notify()
            self.cv.wait()

    __call__ = send
