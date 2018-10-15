import socket
import subprocess
import threading

AVAILABLE_COMMANDS = ('ls', 'cd')

server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_sock.bind(('', 4445))

server_sock.listen(5)  # ????


class ClientThread(threading.Thread):
    """docstring for ClientThread"""
    def __init__(self, sock):
        super(ClientThread, self).__init__()
        self.sock = sock

    def run(self):
        try:
            while True:
                command = self.sock.recv(1024).decode('UTF-8').lstrip()

                if command == 'quit':
                    break

                if command.startswith(AVAILABLE_COMMANDS):
                    res = subprocess.check_output([command])
                    self.sock.send(res)
                else:
                    self.sock.send('Command not available')
        except KeyboardInterrupt:
            self.sock.close()


while True:
    # accept connection
    client_socket, address = server_sock.accept()
    print('Got connection from {}'.format(address))

    client = ClientThread(client_socket)
    client.start()
