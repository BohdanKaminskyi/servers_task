import os

commands = {}


def register_command(command_func):
    commands[command_func.__name__] = command_func

    def wrapper(*args, **kwargs):
        return command_func(*args, **kwargs)
    return wrapper


@register_command
def ls():
    """List directory contents"""
    return os.listdir(os.getcwd())


@register_command
def cd(args):
    """Change the shell working directory

    :param args: Arguments to cd command
    :type args: list
    :raises FileNotFoundError: In case args parameter is not a valid directory
    """
    path = args[0] if args else '../..'
    os.chdir(path)


@register_command
def pwd():
    """Print working directory

    :returns: String representing working directory name
    :rtype: str
    """
    return os.getcwd()
