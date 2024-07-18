import sys
import time
from adafruit_ble import BLERadio
from adafruit_ble.services.nordic import UARTService

DEVICE_NAME = "pyDrone"
address = "C608FC48-9501-7C72-E76C-2E8CC58B448B" # Change this to your drone's BLE address
n = 256
retry = 1

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
                    time.sleep(0.1)
            break
        break

def ble():
    protocol_data = [b'\x01\x6f\x6f\x6f\x6f\x88']

    ble, advertisement = scan()
    ble.connect(advertisement)
    print("Drone Connected")
    print("Racing....")
    while True:
        for i in range(n):
            data = list(map(lambda x:x+i.to_bytes(), protocol_data))
            send(ble, data)

def main():
    ble()

if __name__ == "__main__":
    main()
