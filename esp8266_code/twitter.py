ESSID2 = 'Columbia University'
PASSWORD = ''

import socket, json
import ssd1306b
from machine import I2C, Pin
import time
import socket
import network

def do_connect():
    #import network
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(ESSID2, PASSWORD)
        while not sta_if.isconnected():
            pass
        print('network config:', sta_if.ifconfig())
    return(sta_if.ifconfig()[0])


# Don't forget to set the mode local or normal
def http_get(path, https):
    local = False
    if not local:
        host = 'ec2-54-221-93-111.compute-1.amazonaws.com'
    else:
        host = '9f5c5f0e.ngrok.io'
    if https:
        port = 443
    else:
        port = 80
    addr = socket.getaddrinfo(host, port)[0][-1]
    s = socket.socket()
    s.connect(addr)
    res = ''
    s.send(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host), 'utf8'))
    data = s.recv(100)
    while data:
        data = s.recv(100)
        res += str(data, 'utf8')
    s.close()
    return(res)



