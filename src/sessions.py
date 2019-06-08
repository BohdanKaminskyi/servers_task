import asyncio
import socket

from src.commands.commands_processor import CommandProcessor
from src.response_handler import Response
from src.commands.commands import CommandBroker


class ClientSession:
    def __init__(self, sock: socket.socket):
        self.sock = sock
        self.events = CommandBroker()

    def send(self, data: str, encoding: str = 'utf-8'):
        """Send data over the socket

        :param data: Response to send to client
        :type data: str
        :param encoding: Data encoding
        :type encoding: str
        """
        self.events.notify(data)
        self.sock.send(data.encode(encoding))

    def receive(self, bufsize: int = 1024):
        """Receive response from the socket

        :param bufsize: The maximum amount of data to be received at once
        :type bufsize: int
        :returns: Response object
        :rtype: Response
        """
        response_string = self.sock.recv(bufsize).decode('utf-8')
        return Response.decode(response_string)


class ServerSession:
    def __init__(self, sock: socket.socket):
        self.sock = sock

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

            response = CommandProcessor.process_command(command)
            self.send(response)


class AsyncServerSession:
    def __init__(self, sock: socket.socket, loop: asyncio.AbstractEventLoop):
        self.sock = sock
        self.loop = loop

    async def send(self, response: Response):
        """Send response to client

        :param response: Response to send to client
        :type response: Response
        """
        await self.loop.sock_sendall(self.sock, response.encode('utf-8'))

    async def receive(self, bufsize: int = 1024):
        """Receive data from the socket

        :param bufsize: The maximum amount of data to be received at once
        :type bufsize: int
        :returns: String representing received data
        :rtype: str
        """
        message = await self.loop.sock_recv(self.sock, bufsize)
        return message.decode('utf-8')

    async def server_loop(self):
        """Handle client commands"""
        while True:
            command = await self.receive()
            command = command.lstrip().split()

            response = CommandProcessor.process_command(command)
            await self.send(response)
