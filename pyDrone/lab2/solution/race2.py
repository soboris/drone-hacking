import sys
import time
from adafruit_ble import BLERadio
from adafruit_ble.services.nordic import UARTService

DEVICE_NAME = "pyDrone"
address = "C608FC48-9501-7C72-E76C-2E8CC58B448B" # Change this to your drone's BLE address
n = 256
retry = 1

keys = [22, 54, 86, 118, 150, 182, 214, 246]

def scan():
    ble = BLERadio()
    print("Scanning")
    found = set()
    scan_responses = set()
    for advertisement in ble.start_scan():
        addr = advertisement.address
        print(addr, advertisement)
        print("\t" + repr(advertisement))
        if (addr not in scan_responses):
            scan_responses.add(addr)
            # if (advertisement.complete_name == DEVICE_NAME and addr.string == address):
            if (advertisement.complete_name == DEVICE_NAME):
                found.add(addr)
                break
        else:
            continue
    print("Scan Done")
    return ble, advertisement

def send(ble, data):
    while (ble.connected):
        for connection in ble.connections:
            if UARTService not in connection:
                continue
            uart = connection[UARTService]
            for entry in data:
                for i in range(retry):
                    uart.write(entry)
                    res = uart.readline()
                    if res and res != b'\x00':
                        print("states recevied")
                        print (res)
                        return True
            break
        break
    return False

def ble():
    protocol_data = [b'\x01\x6f\x6f\x6f\x6f\x88']

    ble, advertisement = scan()
    ble.connect(advertisement)
    print("Drone Connected")
    print("Racing....")
    while True:
        for k in keys:
            for i in range(n):
                xored = [_a ^ _b for _a, _b in zip(i.to_bytes(), k.to_bytes())][0]
                data = list(map(lambda x:x+xored.to_bytes(), protocol_data))
                if send(ble, data):
                    key = k
                    counter = i
                    while True:
                        if counter == n - 1:
                            counter = 0
                        counter += 1
                        xored = [_a ^ _b for _a, _b in zip(counter.to_bytes(), key.to_bytes())][0]
                        data = list(map(lambda x:x+xored.to_bytes(), protocol_data))
                        if not send(ble, data):
                            break

def main():
    ble()

if __name__ == "__main__":
    main()
