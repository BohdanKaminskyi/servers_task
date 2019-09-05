import asyncio
import json
import socket

from src.commands.commands_processor import CommandProcessor
from src.requests.response_handler import Response
from src.commands.commands import CommandBroker
from src.manager import MessageManager
from src.requests.serializers import RequestJSONSerializer


class ClientSession:
    def __init__(self, sock: socket.socket):
        self.sock = sock
        self.events = CommandBroker()

    # TODO: we need to send requests not strings
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
        print('heheehhehehehhe')
        response_string = self.sock.recv(bufsize).decode('utf-8')
        print('hehesssss')
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

    def receive(self, bufsize: int = 1024) -> bytes:
        """Receive data from the socket

        :param bufsize: The maximum amount of data to be received at once
        :type bufsize: int
        :returns: String representing received data
        :rtype: bytes
        """
        message = self.sock.recv(bufsize)
        print(f'got message: {message}')
        return message

    def server_loop(self):
        """Handle client commands"""
        manager = MessageManager(serializer=RequestJSONSerializer,
                                 executor='',
                                 protocol='')
        while True:

            message = self.receive().decode('utf-8')  #.lstrip().split()
            # 1. check header
            # 2. deserialize message if header is ok
            # 3. CommandProcessor.process_command(command)
            # 4. serialize response
            # 5. send response
            # questions: what if client sends some shit?

            # doing duplicate work, as `validate_header` already deserializes full message
            if manager.validate_header(message):
                request = manager.get_request(message)
                print(request)
                response = Response(content=request, status=200)
                self.send(response.encode())
            else:
                print('Cannot find header `Auth`')
                self.send('BAD REQUEST')


class AsyncServerSession:
    def __init__(self, sock: socket.socket):
        self.sock = sock
        self.loop = asyncio.get_running_loop()

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
