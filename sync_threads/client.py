import sys
import socket
from commands import Commands, CommandNotFoundError
from response_handler import Response


class ClientDisconnectedError(Exception):
    pass


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


class ClientSession:
    def __init__(self, sock: socket.socket):
        self.sock = sock

    def send(self, data: str, encoding: str='utf-8'):
        """Send data over the socket

        :param data: Response to send to client
        :type data: str

        :param encoding: Data encoding
        :type encoding: str
        """
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

    def loop(self):
        """Handle client sending, receiving data"""
        try:
            while True:
                message = input('>>>')

                if not message:
                    continue

                if message.lower() == 'quit':
                    message = 'quit'
                    self.send(message)
                    self.sock.close()
                    break

                if message.lower().startswith('history'):
                    # print('\n'.join(map(lambda command: '   ' + command, Commands.execute('history', command_history))))
                    continue

                self.send(message)

                response = self.receive()
                print(response)

        except KeyboardInterrupt:
            message = 'quit'
            self.send(message)
            self.sock.close()
            sys.exit()


if __name__ == "__main__":
    PORT = 4445

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # reuse socket
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # sock.connect(('93.77.147.252', PORT)) # uncomment for multi-machine use
    sock.connect(('', PORT))


    client_session = ClientSession(sock)
    client_session.loop()

