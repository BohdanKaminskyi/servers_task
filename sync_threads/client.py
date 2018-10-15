import socket

PORT = 4445

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# reuse socket
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

sock.connect(('93.77.147.252', PORT))


while True:
    try:
        message = input('>>>')
        sock.send(message.encode('UTF-8'))

        response = sock.recv(1024)
        print(response.decode('UTF-8'))
    except KeyboardInterrupt:
        sock.close()
