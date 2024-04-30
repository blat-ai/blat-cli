import argparse
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


def run(args: argparse.Namespace):
    """
    Creates the distribution package for the project.
    """
    pypi_name = args.pypi_name
    execute("poetry", "build", "--format", "wheel", "--no-interaction")
    if args.publish:
        execute("poetry", "config", f"repositories.{pypi_name}", args.pypi_repository)
        execute("poetry", "config", f"repositories.{pypi_name}")
        if args.pypi_token:
            execute("poetry", "config", f"pypi-token.{pypi_name}", args.pypi_token)
        execute("poetry", "publish", "--no-interaction", "-r", pypi_name)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--publish", help="Publish the package to PyPI.", action="store_true", default=False)
    parser.add_argument("--pypi-repository", help="The PyPI repository to upload the package to.")
    parser.add_argument("--pypi-token", help="The PyPI token to authenticate the upload.")
    parser.add_argument("--pypi-name", help="The name of the PyPI repository to upload the package to.", default="pypi")
    with curr_dir(project_folder):
        run(parser.parse_args())
