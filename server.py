import argparse
import asyncio

from src.sessions import AsyncServerSession
from src.workers import SyncWorker, TaskSubmitter
from concurrent.futures import ProcessPoolExecutor
from src.socket_config import ServerSocket


parser = argparse.ArgumentParser(description='TCP server for handling basic unix commands')

parser.add_argument('--serve_async', action="store_true", default=False)


ADDRESS, PORT = '', 4445


async def run_server_async(loop: asyncio.AbstractEventLoop):
    sock = ServerSocket(ADDRESS, PORT, is_blocking=False)

    try:
        while True:
            client_socket, address = await loop.sock_accept(sock.sock)
            print(f'Got connection from {address}')
            loop.create_task(AsyncServerSession(client_socket, loop).server_loop())
    except KeyboardInterrupt:
        pass


def run_server_sync():
    sock = ServerSocket(ADDRESS, PORT)
    pool = ProcessPoolExecutor(max_workers=5)
    launcher = TaskSubmitter(pool)

    try:
        while True:
            client_socket, address = sock.sock.accept()
            print(f'Got connection from {address}')

            worker = SyncWorker(client_socket)
            launcher.submit(worker)

    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    args = parser.parse_args()

    if args.serve_async:
        print('Running async...')
        loop = asyncio.get_event_loop()
        loop.create_task(run_server_async(loop))
        loop.run_forever()

    else:
        print('Running sync...')
        run_server_sync()
