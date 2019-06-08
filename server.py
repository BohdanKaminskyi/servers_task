import socket
from threading import Thread
from multiprocessing import Process
from typing import Union
from response_handler import Response
from client import Client, ClientDisconnectedError
from workers import SyncWorker, ThreadLauncher
from concurrent.futures import ThreadPoolExecutor

server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_sock.bind(('', 4445))

server_sock.listen(5)



if __name__ == '__main__':
    pool = ThreadPoolExecutor(max_workers=5)
    launcher = ThreadLauncher(pool)

    try:
        while True:
            client_socket, address = server_sock.accept()
            print(f'Got connection from {address}')

            # worker = Thread()
            # server_session = ServerSession(sock=client_socket, worker=worker)

            worker = SyncWorker(client_socket)
            launcher.submit(worker)

            # try:
            #     server_session.start()
            # except ClientDisconnectedError:
            #     print(f'Connection to {address} is lost...')

    except KeyboardInterrupt:
        pass


# worker does the job