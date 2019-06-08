import socket
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from response_handler import Response
from client import Client

class ServerSession:
    def __init__(self, sock: socket.socket):
        self.sock = sock
        # self.worker = worker
        # self.worker.run = self.loop

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


class Worker:
    def __init__(self):
        # raise NotImplemented
        pass

class SyncWorker(Worker):
    def __init__(self, sock: socket.socket):
        super().__init__()
        self.sock = sock

    def start(self):
        session = ServerSession(self.sock)
        session.loop()


class ThreadLauncher:
    def __init__(self, pool=ThreadPoolExecutor):
        self.pool = pool

    def submit(self, worker: SyncWorker):
        self.pool.submit(worker.start)
