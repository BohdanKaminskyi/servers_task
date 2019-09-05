from src.commands.commands import Commands, CommandNotFoundError
from src.requests.response import Response


class ClientDisconnectedError(Exception):
    pass


class CommandProcessor:
    """Handle commands"""

    @staticmethod
    def process_command(command) -> Response:
        if not command:
            return Response(status=200, data='')

        command, args = command[0].lower(), command[1:]

        if command == 'quit':
            raise ClientDisconnectedError

        try:
            command_output = Commands.execute(command, *args)
            response = Response(
                status=200,
                data=command_output
            )
        except CommandNotFoundError:
            response = Response(
                status=404,
                data=f'{command}: command not found'
            )

        return response