from commands import Commands, CommandNotFoundError
from response_handler import Response


class ClientDisconnectedError(Exception):
    pass


class Client:
    """Handle client commands"""

    @staticmethod
    def process_command(command) -> Response:
        if not command:
            return Response(status=200, content='')

        command, args = command[0].lower(), command[1:]

        if command == 'quit':
            raise ClientDisconnectedError

        try:
            command_output = Commands.execute(command, *args)
            response = Response(
                status=200,
                content=command_output
            )
        except CommandNotFoundError:
            response = Response(
                status=404,
                content=f'{command}: command not found'
            )

        return response