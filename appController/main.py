import socket

host = "192.168.4.1" # Change this to your drone's WiFi AP server address
port = 2390 # Change this to your drone's WiFi AP server port

def main():
    protocol_data = [b'\x01\x6f\x6f\x6f\x6f\x18', b'\x01\x6f\x6f\x6f\x6f\x48']

    while True:
        for entry in protocol_data:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect((host, port))
                sock.sendall(entry)
                data = sock.recv(1024)
                print("Received:")
                print(data)

if __name__ == '__main__':
    main()
