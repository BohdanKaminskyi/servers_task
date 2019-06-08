import socket
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from src.sessions import ServerSession
from typing import Union


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


class TaskSubmitter:
    def __init__(self, pool: Union[ThreadPoolExecutor, ProcessPoolExecutor]):
        self.pool = pool

    def submit(self, worker: SyncWorker):
        self.pool.submit(worker.start)
