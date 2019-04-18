import socket
from response_handler import Response
from commands import Commands

PORT = 4445
# TODO add logic to handle responses

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# reuse socket
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# sock.connect(('93.77.147.252', PORT)) # uncomment for multi-machine use
sock.connect(('', PORT))


if __name__ == "__main__":
    command_history = CommandsHistory()

    while True:
        try:
            message = input('>>>')

            if not message:
                continue

            if message.lower() == 'quit':
                message = 'quit'
                sock.send(message.encode('utf-8'))
                sock.close()
                break

            if message.lower().startswith('history'):
                print('\n'.join(map(lambda command: '   ' + command, Commands.execute('history', command_history))))
                command_history.append(message)
                continue

            command_history.append(message)
            sock.send(message.encode('utf-8'))

            response = sock.recv(1024)
            print(Response.decode(response))

        except KeyboardInterrupt:
            message = 'quit'
            sock.send(message.encode('utf-8'))
            sock.close()
            break
