import os

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


class CommandsHistory:
    def __init__(self):
        self._history = []

    def show_history(self):
        return self._history

    def append(self, command: str):
        self._history.append(command)


class HistoryViewer:
    pass


class CommandHandler:
    def __init__(self, current_path:str, history: CommandsHistory):
        self._current_path = current_path
        self._history = history



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
