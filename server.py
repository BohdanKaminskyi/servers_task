from workers import SyncWorker, ThreadLauncher
from concurrent.futures import ThreadPoolExecutor
from socket_config import ServerSocket


if __name__ == '__main__':
    ADDRESS, PORT = '', 4445
    sock = ServerSocket(ADDRESS, PORT)
    pool = ThreadPoolExecutor(max_workers=5)
    launcher = ThreadLauncher(pool)

    try:
        while True:
            client_socket, address = sock.sock.accept()
            print(f'Got connection from {address}')

            worker = SyncWorker(client_socket)
            launcher.submit(worker)

    except KeyboardInterrupt:
        pass
