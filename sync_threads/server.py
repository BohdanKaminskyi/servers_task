import socket
import os
import threading
from response_handler import ResponseHandler

server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_sock.bind(('', 4445))

server_sock.listen(5)  # ????


AVAILABLE_COMANDS = ['cd', 'quit']


class ClientThread(threading.Thread):
    """docstring for ClientThread"""

    def __init__(self, sock):
        super(ClientThread, self).__init__()
        self.sock = sock

    def send(self, data):
        self.sock.send(data.encode('UTF-8'))

    # TODO keyboard interrupt not closing socket...
    # TODO refactor, divide into individual functions
    def run(self):
        try:
            while True:
                command = self.sock.recv(1024).decode('UTF-8').lstrip().split()

                if not command:
                    continue

                command, params = command[0].lower(), command[1:]

                if command in AVAILABLE_COMANDS:
                    if command == 'quit':
                        break

                    if command == 'cd':
                        try:
                            path = params[0] if params else '../..'
                            os.chdir(path)

                            response_data = {
                                'status': 200,
                                'data': ''
                            }
                        except FileNotFoundError:
                            response_data = {
                                'status': 404,
                                'message': 'No such file or directory'
                            }

                        response = ResponseHandler.encode(response_data)
                        self.send(response)

                else:
                    response_data = {
                        'status': 404,
                        'message': f'{command}: command not found'
                    }

                    response = ResponseHandler.encode(response_data)
                    self.send(response)

        except KeyboardInterrupt:
            self.sock.close()


while True:
    client_socket, address = server_sock.accept()
    print('Got connection from {}'.format(address))

    client = ClientThread(client_socket)
    client.start()
