import socket


class Socket:
    def __init__(self, host='', port=4445):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.host = host
        self.port = port


class ServerSocket(Socket):
    def __init__(self, host='', port=4445, is_blocking: bool = True):
        super().__init__(host, port)
        self.sock.bind((self.host, self.port))
        self.sock.listen(5)
        self.sock.setblocking(is_blocking)


class ClientSocket(Socket):
    def __init__(self, host='', port=4445):
        super().__init__(host, port)
        self.sock.connect((self.host, self.port))
