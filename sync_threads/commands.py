import os


def ls():
    """
    List directory contents
    """
    return os.listdir(os.getcwd())


def cd(args):
    """
    Change the shell working directory.
    """
    path = args[0] if args else '../..'
    os.chdir(path)
