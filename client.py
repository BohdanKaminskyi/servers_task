import sys
from commands import CommandHistory
from helpers import HistoryViewer
from sessions import ClientSession
from socket_config import ClientSocket


if __name__ == "__main__":
    ADDRESS, PORT = '', 4445
    sock = ClientSocket(ADDRESS, PORT)
    client_session = ClientSession(sock.sock)

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
