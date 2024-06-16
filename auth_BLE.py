import bluetooth,ble_simple_peripheral,time
import drone
import os
import binascii
import auth
from fragproc import Packet
from fragbin import Bin

f = open('blackbox', 'w')

bin = Bin()

# Headless mode
d = drone.DRONE(flightmode = 0, debug = 1)

authenticated = False

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

ble = bluetooth.BLE()

p = ble_simple_peripheral.BLESimplePeripheral(ble,name='pyDrone')

def authProtoHdlr(recvData):
    if bytearray(recvData) == auth.getHelloMsg():
        global authenticated
        authenticated = False
        global authData
        authData = auth.authReq()
        p.send(authData)
        print("Received Hello Message")
    if auth.isAuthCLA(recvData):
        global bin
        bin.putFragment(recvData)
        try:
            recvPacket = bin.checkPacket()
            if recvPacket:
                if auth.verifyToken(authData, recvPacket):
                    global counter
                    counter, syncData = auth.syncCounter()
                    print("sending syncData")
                    p.send(syncData)
                    # Slow operations
                    '''
                    syncPacket = Packet(syncData)
                    global syncFragments
                    syncFragments = syncPacket.frag()
                    # print(binascii.hexlify(syncFragments[0]))
                    # p.send(syncFragments[0])
                    for syncFragment in syncFragments:
                        print(binascii.hexlify(syncFragment))
                        p.send(syncFragment)
                        time.sleep_ms(100)
                    '''
                    global authenticated
                    authenticated = True
                    print("Authenticated")
        except Exception as e:
            print(e.message)

def on_rx(text):
    print("received data")
    print(binascii.hexlify(text))
    # Dummy data to trigger exception that allows data to be sent, weird bug to be investigated.
    p.send(b'\x00')

    if not authenticated or bytearray(text) == auth.getHelloMsg():
        authProtoHdlr(text)
        return

    # Slow operations
    '''
    if bytearray(text) == b'ack':
        global syncFragments
        syncFragments.remove(syncFragments[0])
        print(binascii.hexlify(syncFragments[0]))
        p.send(bytes(syncFragments[0]))
        return
    '''

    if text[0] == 222: # 0xde to disconnect all connected central
        p.disconnect_all()
        return

    control_data = [None]*4
    
    # Debug only
    print("RX:", binascii.hexlify(text).decode())
    
    # Debug only
    for i in range(len(text)):
        print(i,text[i])

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

    p.send(bytes(state_buf)) # send back flight attitude data

p.on_write(on_rx)
