import os


class Commands:
    commands = {}

    @classmethod
    def register(cls, command_func):
        cls.commands[command_func.__name__] = command_func
        return command_func

    @classmethod
    def execute(cls, *argv, command, args):
        command_func = cls.commands.get(command, KeyError(f'unknown command: {command}'))
        return command_func(args)


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
