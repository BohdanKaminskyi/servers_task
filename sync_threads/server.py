import socket
from threading import Thread
from multiprocessing import Process
from typing import Union
from commands import Commands, CommandNotFoundError
from response_handler import Response

server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_sock.bind(('', 4445))

server_sock.listen(5)

ClientDisconnectedError = Exception


class Client:
    """Handle client commands"""

    @staticmethod
    def process_command(command) -> Response:
        if not command:
            return Response(status=200, content='')

        command, args = command[0].lower(), command[1:]

        if command == 'quit':
            raise ClientDisconnectedError

        try:
            command_output = Commands.execute(command=command, *args)
            response = Response(status=200, content=command_output)
        except CommandNotFoundError:
            response = Response(status=404, content=f'{command}: command not found')

        return response


class Session:
    def __init__(self, sock: socket.socket, worker: Union[Thread, Process]):
        self.sock = sock
        self.worker = worker
        self.worker.run = self.loop

    def send(self, response: Response):
        """Send response to client

        :param response: Response to send to client
        :type response: Response
        """
        self.sock.send(response.encode('utf-8'))

    def receive(self, bufsize: int = 1024):
        """Receive data from the socket

        :param bufsize: The maximum amount of data to be received at once
        :type bufsize: int
        :returns: String representing received data
        :rtype: str
        """
        return self.sock.recv(bufsize).decode('utf-8')

    def loop(self):
        """Handle client commands"""
        while True:
            command = self.receive().lstrip().split()

            response = Client.process_command(command)

            self.send(response)

    def start(self):
        """"""
        return self.worker.start()


if __name__ == '__main__':
    try:
        while True:
            client_socket, address = server_sock.accept()
            print('Got connection from {}'.format(address))

            worker = Thread()
            client_session = Session(sock=client_socket, worker=worker)
            client_session.start()

    except KeyboardInterrupt:
        pass
