import socket
import os
import threading
import commands
from response_handler import Response

server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_sock.bind(('', 4445))

server_sock.listen(5)  # ????


AVAILABLE_COMANDS = ('cd', 'ls', 'dir', 'quit')


class ClientThread(threading.Thread):
    """Client thread to handle individual clients"""

    def __init__(self, sock):
        super().__init__()
        self.sock = sock

    def send(self, response):
        """Send response to client

        :param response: Response to send to client
        :type response: response
        """
        self.sock.send(response.encode('utf-8'))

    def receive(self, bufsize=1024):
        """Receive data from the socket.

        :param bufsize: The maximum amount of data to be received at once
        :type bufsize: int
        :returns: String representing received data
        :rtype: str
        """
        return self.sock.recv(bufsize).decode('utf-8')

    def run(self):
        """Handle TODO"""
        try:
            while True:
                command = self.receive().lstrip().split()

                if not command:
                    continue

                command, args = command[0].lower(), command[1:]

                if command in AVAILABLE_COMANDS:
                    if command == 'quit':
                        self.sock.close()
                        break

                    if command == 'cd':
                        try:
                            commands.cd(args)
                            response = Response(status=200, content='')

                        except FileNotFoundError:
                            response = Response(status=404, content='No such file or directory')

                    if command in ('ls', 'dir'):
                        directory_items = commands.ls()
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
