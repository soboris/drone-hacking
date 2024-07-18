import sys
import time
import socket
import asyncio
from adafruit_ble import BLERadio
from adafruit_ble.services.nordic import UARTService

DEVICE_NAME = "pyDrone"
address = "C608FC48-9501-7C72-E76C-2E8CC58B448B" # Change this to your drone's BLE address

host = "192.168.4.1" # Change this to your drone's WiFi AP server address
port = 2390 # Change this to your drone's WiFi AP server port

retry = 5

def ble():
    protocol_data = [b'\x01\x6f\x6f\x6f\x6f\x18', b'\x01\x6f\x6f\x6f\x6f\x48']

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
            if (advertisement.complete_name == DEVICE_NAME and addr.string == address):
                found.add(addr)
                break
        else:
            continue
    print("Scan Done")

    ble.connect(advertisement)
    print("Drone Connected")

    while (ble.connected):
        for connection in ble.connections:
            if UARTService not in connection:
                continue
            uart = connection[UARTService]
            for entry in protocol_data:
                for i in range(retry):
                    uart.write(entry)
                    time.sleep(0.5)
            break
        break

def wifi():
    protocol_data = [b'\x01\x6f\x6f\x6f\x6f\x18', b'\x01\x6f\x6f\x6f\x6f\x48']

    for entry in protocol_data:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((host, port))
            sock.sendall(entry)
            data = sock.recv(1024)
            print("Received:")
            print(data)

def main():
    if len(sys.argv) > 1:
        fn = sys.argv[1]
        if fn.lower() == "ble":
            ble()
        if fn.lower() == "wifi":
            wifi()
    else:
        print("Program argument (case insensitive): ble/wifi")

if __name__ == "__main__":
    main()
