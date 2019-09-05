from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from src.sessions.sessions import ServerSession, AsyncServerSession
import asyncio
from typing import Union


class Worker:
    def __init__(self, session: Union[ServerSession, AsyncServerSession]):
        self.session = session

    def start(self):
        raise NotImplemented


class SyncWorker(Worker):
    def start(self):
        self.session.server_loop()


class AsyncWorker(Worker):
    async def start(self):
        await self.session.server_loop()


class TaskManager:
    def __init__(self, strategy_obj: Union[ThreadPoolExecutor, ProcessPoolExecutor, asyncio.AbstractEventLoop]):
        self.strategy_obj = strategy_obj
        self.is_async = isinstance(self.strategy_obj, asyncio.AbstractEventLoop)

        if self.is_async:
            self.submit = lambda worker: self.strategy_obj.create_task(worker.start())
        else:
            self.submit = lambda worker: self.strategy_obj.submit(worker.start)
