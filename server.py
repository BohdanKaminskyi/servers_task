import argparse
import asyncio

from src.sessions import ServerSession, AsyncServerSession
from src.workers import SyncWorker, AsyncWorker, TaskManager
from concurrent.futures import ProcessPoolExecutor
from src.socket_config import ServerSocket
from dbalchemy import Session
from dbalchemy.models import User


parser = argparse.ArgumentParser(description='TCP server for handling basic unix commands')

parser.add_argument('--serve_async', action="store_true", default=False)


ADDRESS, PORT = '', 4445


async def run_server_async():
    loop = asyncio.get_running_loop()
    sock = ServerSocket(ADDRESS, PORT, is_blocking=False)

    launcher = TaskManager(loop)

    try:
        while True:
            client_socket, address = await loop.sock_accept(sock.sock)
            print(f'Got connection from {address}')

            worker = AsyncWorker(AsyncServerSession(client_socket))
            launcher.submit(worker)

    except KeyboardInterrupt:
        pass


def run_server_sync():
    sock = ServerSocket(ADDRESS, PORT)
    pool = ProcessPoolExecutor(max_workers=5)
    launcher = TaskManager(pool)

    try:
        while True:
            client_socket, address = sock.sock.accept()
            print(f'Got connection from {address}')

            worker = SyncWorker(ServerSession(client_socket))
            launcher.submit(worker)

    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    args = parser.parse_args()
    session = Session()

    print(session.query(User).all())

    #
    # if args.serve_async:
    #     print('Running async...')
    #     loop = asyncio.get_event_loop()
    #     loop.create_task(run_server_async())
    #     loop.run_forever()
    #
    # else:
    #     print('Running sync...')
    #     run_server_sync()
