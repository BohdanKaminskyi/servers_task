import os


def ls():
    """List directory contents"""
    return os.listdir(os.getcwd())


def cd(args):
    """Change the shell working directory

    :param args: Arguments to cd command
    :type args: list
    :raises FileNotFoundError: In case args parameter is not a valid directory
    """
    path = args[0] if args else '../..'
    os.chdir(path)


def pwd():
    """Print working directory

    :returns: String representing working directory name
    :rtype: str
    """
    return os.getcwd()
