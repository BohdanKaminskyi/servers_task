import socket
from threading import Thread
from multiprocessing import Process
from typing import Type, Union
from commands import Commands, CommandNotFoundError
from response_handler import Response

server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_sock.bind(('', 4445))

server_sock.listen(5)


class Client:
    """Handle individual clients"""

    def __init__(self, sock, concurrency_strategy: Union[Type[Thread], Type[Process]]):
        super().__init__()
        self.sock = sock
        self.concurrency_strategy = concurrency_strategy

    def send(self, response):
        """Send response to client

        :param response: Response to send to client
        :type response: response
        """
        self.sock.send(response.encode('utf-8'))

    def receive(self, bufsize=1024):
        """Receive data from the socket

        :param bufsize: The maximum amount of data to be received at once
        :type bufsize: int
        :returns: String representing received data
        :rtype: str
        """
        return self.sock.recv(bufsize).decode('utf-8')

    def run(self):
        """Handle client commands"""
        while True:
            command = self.receive().lstrip().split()

            if not command:
                continue

            command, args = command[0].lower(), command[1:]

            if command == 'quit':
                print(f'Client {self.sock.getpeername()} disconnected')
                self.sock.close()
                break

            try:
                command_output = Commands.execute(command=command, args=args)
                response = Response(status=200, content=command_output)
            except CommandNotFoundError:
                response = Response(status=404, content=f'{command}: command not found')

            self.send(response)

    def start(self):
        """"""
        return self.concurrency_strategy(target=self.run).start()


if __name__ == '__main__':
    try:
        while True:
            client_socket, address = server_sock.accept()
            print('Got connection from {}'.format(address))

            client = Client(sock=client_socket, concurrency_strategy=Thread)
            client.start()
    except KeyboardInterrupt:
        pass
