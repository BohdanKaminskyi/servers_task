import os
from queue import Queue


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


class CommandBroker:
    def __init__(self):
        self.__listeners = set()

    def subscribe(self, listener):
        self.__listeners.add(listener)

    def unsubscribe(self, listener):
        self.__listeners.remove(listener)

    def notify(self, command):
        for listener in self.__listeners:
            listener.update(command)


class CommandHistory:
    def __init__(self, history_size: int = 100):
        self.history = Queue(maxsize=history_size)

    def update(self, command):
        self.history.put(command)

    def history_items(self, last_items=0):
        history_items = list(self.history.queue)
        return history_items[-last_items:]


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
