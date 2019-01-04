import socket
from response_handler import Response

PORT = 4445
# TODO add logic to handle responses

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# reuse socket
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# sock.connect(('93.77.147.252', PORT)) # uncomment for multi-machine use
sock.connect(('', PORT))

while True:
    try:
        message = input('>>>')

        if message.lower() == 'quit':
            sock.close()
            break

        sock.send(message.encode('utf-8'))

        response = sock.recv(1024)
        print(Response.decode(response))
    except KeyboardInterrupt:
        sock.close()
        break
