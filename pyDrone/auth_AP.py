import auth
import drone
import machine
import sys
import os
import network
import socket
import binascii
import time
import pyDrone_name as pyDrone
from machine import Timer

port = 2390

f = open('blackbox', 'w')

counter = 0
authenticated = False

# Headless mode
d = drone.DRONE(flightmode = 0, debug = 1)

while True:
    # Debug only
    print(d.read_cal_data())

    # Debug only
    if d.read_calibrated():
        print(d.read_cal_data())
        break
    
    time.sleep_ms(100)
    # Remove before flight :P
    break

def startAP():
    ap_if = network.WLAN(network.AP_IF)
    ap_if.active(True)
    ap_if.config(essid=pyDrone.getName(), authmode=0)

    print(ap_if.ifconfig())

startAP()

addr = socket.getaddrinfo('0.0.0.0', port)[0][-1]
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(addr)
sock.listen(1)
print('Listening on ', addr)

def waitConnect():
    while True:
        c, a = sock.accept()
        if c:
            print('Client connected from', a)
            break
    return c

def authProtoHdlr(recvData, c):
    if bytearray(recvData) == auth.getHelloMsg():
        global authenticated
        authenticated = False
        global authData
        authData = auth.authReq()
        c.send(authData)
        print("Received Hello Message")
    if auth.isAuthCLA(recvData):
        try:
            if auth.verifyToken(authData, recvData):
                global counter
                counter, syncData = auth.syncCounter(encrypted=True)
                print("sending syncData")
                c.send(syncData)
                global authenticated
                authenticated = True
                print("Authenticated")
        except Exception as e:
            print(e.message)

def socket_fun(c):
    try:
        text = c.recv(128)

        if not authenticated or bytearray(text) == auth.getHelloMsg():
            authProtoHdlr(text, c)
            return

        global counter
        if not auth.chkIntegrity(text, counter=counter):
            return
        if counter == 2**(auth.getCtrSize()*8) - 1:
            counter = 0
        counter += 1

        control_data = [None]*4

        for i in range(4):
            if  100 < text[i+1] < 155 :
                control_data[i] = 0
                
            elif text[i+1] <= 100 :      
                control_data[i] = text[i+1] - 100
                
            else:
                control_data[i] = text[i+1] - 155
        
        # Debug only
        print('control:', control_data)

        # rol:[-100:100],pit:[-100:100],yaw:[-100:100],thr:[-100:100]
        d.control(rol = control_data[0], pit = control_data[1], yaw = control_data[2], thr = control_data[3])

        if text[5] == 24: # Button Y pressed
            print('Y')
            d.take_off(distance = 120)
            
        if text[5] == 72: # Button A pressed
            print('A')
            d.landing()

        if text[5] == 40: # Button B pressed
            print('B')
            
        if text[5] == 136: # Button X pressed
            print('X')
            d.stop()

        states = d.read_states()
        print('states: ', states)
        state_buf = [None]*18
        for i in range(9):
            for j in range(2):
                if j == 0:
                    state_buf[i*2+j] = int((states[i]+32768)/256)
                else:
                    state_buf[i*2+j] = int((states[i]+32768)%256)
                    
        c.send(bytes(state_buf)) # send back flight attitude data

    except OSError:
        print("Error receiving data")
        pass

while True:
    c = waitConnect()
    socket_fun(c)
    time.sleep_ms(500)
    c.close()
