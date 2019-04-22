import os
from typing import Sequence


CommandNotFoundError = KeyError  # TODO: add implementation


class Commands:
    commands = {}

    @classmethod
    def register(cls, command_func):
        cls.commands[command_func.__name__] = command_func
        return command_func

    @classmethod
    def execute(cls, command, *args):
        try:
            command_func = cls.commands[command]
            return command_func(*args)
        except KeyError:
            raise CommandNotFoundError


class HistoryViewer:
    def __init__(self, history: Sequence[str]):
        self._history = history

    @property
    def as_strings(self):
        return '\n'.join(
            map(
                lambda ind_command: f'{ind_command[0]:>5}  {ind_command[1]}',
                enumerate(self._history, 1)
                )
            )


@Commands.register
def ls(*args):
    """List directory contents"""
    return os.listdir(os.getcwd())


@Commands.register
def cd(*args):
    """Change the shell working directory

    :param args: Arguments to cd command
    :type args: list
    :raises FileNotFoundError: In case args parameter is not a valid directory
    """
    path = args[0] if args else '../..'
    os.chdir(path)


@Commands.register
def pwd(*args):
    """Print working directory

    :returns: String representing working directory name
    :rtype: str
    """
    return os.getcwd()
