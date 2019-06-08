import sys
import socket
from commands import CommandHistory
from helpers import HistoryViewer
from sessions import ClientSession


if __name__ == "__main__":
    PORT = 4445
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # reuse socket
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # sock.connect(('93.77.147.252', PORT)) # uncomment for multi-machine use
    sock.connect(('', PORT))

    client_session = ClientSession(sock)

    history = CommandHistory(history_size=100)
    client_session.events.subscribe(history)

    try:
        while True:
            message = input('>>>')

            if not message:
                continue

            if message.lower() == 'quit':
                message = 'quit'
                client_session.send(message)
                client_session.sock.close()
                break

            if message.lower().startswith('history'):
                print(
                    HistoryViewer(
                        history.history_items()
                    ).as_strings
                )
                continue

            client_session.send(message)

            response = client_session.receive()
            print(response)

    except KeyboardInterrupt:
        message = 'quit'
        client_session.send(message)
        client_session.sock.close()
        sys.exit()
