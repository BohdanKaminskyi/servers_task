import socket
import os
import threading
import json

server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_sock.bind(('', 4445))

server_sock.listen(5)  # ????


# TODO Refactor
def generate_response_json(status=200, message=''):
    return json.dumps(
        {
            'status': status,
            'message': message
        }
    )


# TODO class for sending messages


class ClientThread(threading.Thread):
    """docstring for ClientThread"""
    def __init__(self, sock):
        super(ClientThread, self).__init__()
        self.sock = sock

    def send(self, data):
        self.sock.send(data.encode('UTF-8'))

    def run(self):
        try:
            while True:
                command = self.sock.recv(1024).decode('UTF-8').lstrip().split()

                command, params = command[0], command[1:]

                if command == 'quit':
                    break

                if command == 'cd':
                    try:
                        os.chdir(params[0])
                        response = generate_response_json(200, 'OK')
                    except os.FileNotFoundError:
                        response = generate_response_json(
                            404,
                            'No such file or directory:'
                        )

                    self.send(response.encode('UTF-8'))

        except KeyboardInterrupt:
            self.sock.close()


while True:
    client_socket, address = server_sock.accept()
    print('Got connection from {}'.format(address))

    client = ClientThread(client_socket)
    client.start()
