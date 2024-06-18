import drone
import network,socket,time
from machine import Timer

ssid = '' # Change this to your AP SSID
psk = '' # Change this to your WPA2 password
url = 'http://localhhost/' # Change this to your web server inlcuding the trailing slash or path
port = 80 # Change this to your server port

# Headless mode
d = drone.DRONE(flightmode = 0)

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

sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect(ssid, psk)
time.sleep_ms(10000)

if (sta_if.isconnected()):
    print('Connected')
    print(sta_if.ifconfig())
else:
    raise Exception('Error connecting to ' + ssid)

def proc(text):
    try:
        rol, pit, yaw, thr, cmd = 0, 0, 0, 0, None
        data = text.split()[::-1][0:5][::-1]
        # Debug only
        print(data)
        for i in range(len(data)):
            if data[i].lstrip('-').isdigit():
                if (int(data[i]) >= -100 and int(data[i]) <= 100):
                    if i == 0:
                        rol = int(data[i])
                    if i == 1:
                        pit = int(data[i])
                    if i == 2:
                        yaw = int(data[i])
                    if i == 3:
                        thr = int(data[i])
            if isinstance(data[i], str):
                if i == 4:
                    cmd = data[i]

        d.control(rol = rol, pit = pit, yaw = yaw, thr = thr)
        states = d.read_states()
        # Debug only
        print('rol:', rol, 'pit:', pit, 'yaw:', yaw, 'thr', thr, 'cmd:', cmd)
        print('states: ', states)
        if cmd.upper() == 'TAKEOFF':
            d.take_off(distance = 120)
            print('Taking off')
        if cmd.upper() == 'LAND':
            d.landing()
            print('landing')
        if cmd.upper() == 'STOP':
            d.stop()
            print('stopping')
        if cmd.upper() == 'EXIT':
            return 1
    except:
        print("Corrupted data")
    return 0

def http_get():
    while True:
        try:
            _, _, host, path = url.split('/', 3)
            addr = socket.getaddrinfo(host, port)[0][-1]
            sock = socket.socket()
            sock.connect(addr)
            sock.send(bytes('GET /%s HTTP/1.1\r\nHost: %s\r\nngrok-skip-browser-warning: true\r\n\r\n' % (path, host), 'utf8'))
            data = sock.recv(256)
            exit = proc(str(data, 'utf8'))
            sock.close()
            if exit:
                break
        except:
            print("Network error")

http_get()
