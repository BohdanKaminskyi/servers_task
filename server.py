from src.workers import SyncWorker, TaskSubmitter
from concurrent.futures import ProcessPoolExecutor
from src.socket_config import ServerSocket


if __name__ == '__main__':
    ADDRESS, PORT = '', 4445
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
