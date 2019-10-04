import asyncio
import socket
import traceback
from colorama import Fore, init
init(autoreset=True)

from src.commands.commands_processor import CommandProcessor
from src.requests.response import Response
from src.commands.commands import CommandBroker
from src.requests.serializers import RequestJSONSerializer, ResponseJSONSerializer


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
        response_string = self.sock.recv(bufsize).decode('utf-8')
        return ResponseJSONSerializer.deserialize(response_string)


class ServerSession:
    def __init__(self,
                 sock: socket.socket,
                 request_serializer=RequestJSONSerializer,
                 response_serializer=ResponseJSONSerializer,
                 executor=CommandProcessor):
        self.sock = sock
        self.request_serializer = request_serializer
        self.response_serializer = response_serializer
        self.executor = executor

    def send(self, data: Response):
        """Send response to client

        :param data: Response to send to client
        :type data: str
        """
        self.sock.send(ResponseJSONSerializer.serialize(data).encode('utf-8'))

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

    def _parse_message(self, message: bytes):
        return self.request_serializer.deserialize(message)

    def _validate_header(self, message):
        request = self._parse_message(message)
        headers = request.headers

        if not headers.get('Auth'):
            return False
        return True

    def server_loop(self):
        """Handle client commands"""
        while True:
            try:
                command = self.receive().decode('utf-8').lstrip().split()
                response = CommandProcessor.process_command(command)
                self.send(response)
            except:
                print(Fore.RED + traceback.format_exc())
                self.send(Response(data='Error occured...', status=400))


class AsyncServerSession:
    def __init__(self, sock: socket.socket):
        self.sock = sock
        self.loop = asyncio.get_running_loop()

    async def send(self, response: Response):
        """Send response to client

        :param response: Response to send to client
        :type response: Response
        """
        await self.loop.sock_sendall(self.sock, ResponseJSONSerializer.serialize(response).encode('utf-8'))

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
