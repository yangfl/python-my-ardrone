#!/usr/bin/env python
#coding=utf8
import socket

address = ('127.0.0.1', 5556)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(address)

while True:
    data, addr = s.recvfrom(65535)
    if not data:
        print "client has exist"
        break
    print "received:", repr(data), "from", addr

s.close()
