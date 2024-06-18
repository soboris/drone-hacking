import socket
import auth

host = "192.168.4.1" # Change this to your drone's WiFi AP server address
port = 2390 # Change this to your drone's WiFi AP server port

def socketSend(data):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((host, port))
        sock.sendall(data)
        recvData = sock.recv(1024)
        return recvData

def authProtoHdlr(recvData):
    if auth.isAuthCLA(recvData):
        if auth.isAuthReq(recvData):
            authData = auth.authRes(recvData)
            if authData:
                print("sending authData")
                counter = auth.retCounter(socketSend(authData), encrypted=True)
                if counter:
                    return True, counter
    return False, 0

def main():
    protocol_data = [b'\x01\x6f\x6f\x6f\x6f\x18', b'\x01\x6f\x6f\x6f\x6f\x48']

    recvData = socketSend(auth.getHelloMsg())
    print("Received:")
    print(recvData)
    authenticated, counter = authProtoHdlr(recvData)

    if authenticated:
        print("authenticated")
        while True:
            for entry in protocol_data:
                recvData = socketSend(auth.prepPayload(entry, counter=counter))
                if counter == 2**(auth.getCtrSize()*8) - 1:
                    counter = 0
                counter += 1
                print("Received:")
                print(recvData)

if __name__ == '__main__':
    main()
