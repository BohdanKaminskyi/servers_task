import sys
from src.commands.commands import CommandHistory
from src.helpers import HistoryViewer
from src.sessions import ClientSession
from src.socket_config import ClientSocket


if __name__ == "__main__":
    # let's keep it stupid for now: checking <admin:password> before we go
    username = 'admin'
    password = 'password'
    
    if username != 'admin' or password !='password':
        sys.exit()

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

            # TODO need to identify myself and send some ID to server...
            # 1. we can try identifying by ip+port but then session will be broken in case same user wants to login from another pc..
            # 2. we can add user credentials <login:password> and based on that data identify user and latest command he used or pwd
            # after that we can add tokens etc.
            client_session.send(message)

            response = client_session.receive()
            print(response)

    except KeyboardInterrupt:
        message = 'quit'
        client_session.send(message)
        client_session.sock.close()
        sys.exit()
