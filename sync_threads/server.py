import socket
import os
import threading
from response_handler import Response

server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_sock.bind(('', 4445))

server_sock.listen(5)  # ????


AVAILABLE_COMANDS = ['cd', 'ls', 'dir', 'quit']


class ClientThread(threading.Thread):
    """docstring for ClientThread"""

    def __init__(self, sock):
        super(ClientThread, self).__init__()
        self.sock = sock

    def send(self, response):
        self.sock.send(response.encode('utf-8'))

    # TODO refactor, divide into individual functions
    def run(self):
        try:
            while True:
                command = self.sock.recv(1024).decode('utf-8').lstrip().split()

                if not command:
                    continue

                command, params = command[0].lower(), command[1:]

                if command in AVAILABLE_COMANDS:
                    if command == 'quit':
                        self.sock.close()
                        break

                    if command == 'cd':
                        try:
                            path = params[0] if params else '../..'
                            os.chdir(path)

                            response = Response(status=200, content='')

                        except FileNotFoundError:
                            response = Response(status=404, content='No such file or directory')

                    if command in ('ls', 'dir'):
                        directory_items = os.listdir(os.getcwd())
                        response = Response(status=200, content='\n'.join(directory_items))

                else:
                    response = Response(status=404, content=f'{command}: command not found')

                self.send(response)

        except KeyboardInterrupt:
            self.sock.close()


while True:
    client_socket, address = server_sock.accept()
    print('Got connection from {}'.format(address))

    client = ClientThread(client_socket)
    client.start()
