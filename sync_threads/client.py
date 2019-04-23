import sys
import socket
from commands import Commands, CommandNotFoundError
from response_handler import Response
from queue import Queue
from helpers import HistoryViewer


class CommandBroker:
    def __init__(self):
        self.__listeners = set()

    def subscribe(self, listener):
        self.__listeners.add(listener)

    def unsubscribe(self, listener):
        self.__listeners.remove(listener)

    def notify(self, command):
        for listener in self.__listeners:
            listener.update(command)


class CommandHistory:
    def __init__(self, history_size: int = 100):
        self.history = Queue(maxsize=history_size)

    def update(self, command):
        self.history.put(command)

    def history_items(self, last_items=0):
        history_items = list(self.history.queue)
        return history_items[-last_items:]


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
            command_output = Commands.execute(command, *args)
            response = Response(
                status=200,
                content=command_output
            )
        except CommandNotFoundError:
            response = Response(
                status=404,
                content=f'{command}: command not found'
            )

        return response


class ClientSession:
    def __init__(self, sock: socket.socket, history_size: int = 100):
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


if __name__ == "__main__":
    PORT = 4445
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # reuse socket
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # sock.connect(('93.77.147.252', PORT)) # uncomment for multi-machine use
    sock.connect(('', PORT))

    client_session = ClientSession(sock)

    history = CommandHistory()
    client_session.events.subscribe(history)

    try:
        while True:
            message = input('>>>')

            if not message:
                continue

            if message.lower() == 'quit':
                message = 'quit'
                client_session.send(message)
                client_session.sock.close()
                break

            if message.lower().startswith('history'):
                print(HistoryViewer(history.history_items()).as_strings)
                continue

            client_session.send(message)

            response = client_session.receive()
            print(response)

    except KeyboardInterrupt:
        message = 'quit'
        client_session.send(message)
        client_session.sock.close()
        sys.exit()
