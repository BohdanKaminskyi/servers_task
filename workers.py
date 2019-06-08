import socket
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from sessions import ServerSession


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
