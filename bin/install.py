import os
import subprocess
from contextlib import contextmanager
from os import path

project_folder = path.dirname(path.dirname(path.abspath(__file__)))


@contextmanager
def curr_dir(path: str):
    """
    Sets the current directory to the given path while inside context manager. Then goes back to the original directory.

    :param path: The path of the directory to change to.
    """
    cwd = os.getcwd()
    try:
        os.chdir(path)
        yield
    finally:
        os.chdir(cwd)


def execute(*command_args: str):
    """
    Executes the given command in the shell.

    :param command_args: The command and its arguments to execute.
    """
    return subprocess.run(" ".join(command_args), shell=True, check=True)


def run():
    """
    Installs the dependencies of the project and the project itself.
    """
    execute("pip", "install", "poetry")
    execute("poetry", "config", "virtualenvs.create", "false")
    execute("poetry", "install")
    execute("blat", "init-system")


if __name__ == "__main__":
    with curr_dir(project_folder):
        run()
