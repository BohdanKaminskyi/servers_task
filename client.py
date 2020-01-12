import sys
from src.commands.commands import CommandHistory
from src.helpers import HistoryViewer
from src.sessions.sessions import ClientSession
from src.socket_config import ClientSocket
import json
from src.requests.request import Request
from src.requests.serializers import RequestJSONSerializer


if __name__ == "__main__":
    username = 'admin'
    password = 'password'
    
    if username != 'admin' or password !='password':
        sys.exit()

    ADDRESS, PORT = '', 4445
    sock = ClientSocket(ADDRESS, PORT)
    client_session = ClientSession(sock.sock)

    history = CommandHistory(history_size=100)
    client_session.events.subscribe(history)

    data = {
        'command': 'something'
    }

    headers = {
        'Auth': 'aaa_password_aaa'
    }

    request = Request(data=data, headers=headers)
    serialized_request = RequestJSONSerializer.serialize(request)

    client_session.send(serialized_request)

    response = client_session.receive()
    print(response)

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
