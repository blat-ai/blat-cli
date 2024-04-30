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
    Executes the linting, type checking and code formatting of the project.

    :param args: The arguments to use to run the checks.
    """
    poetry_command = ["poetry", "run"]
    ruff_command = poetry_command + ["ruff"]
    ruff_py_version = f"py{args.python_version.replace('.', '')}"

    ruff_check = ruff_command + ["check", project_folder, "-n", "--target-version", ruff_py_version]
    execute(*ruff_check)

    ruff_format = ruff_command + ["format", project_folder, "--check", "-n", "--target-version", ruff_py_version]
    execute(*ruff_format)

    mypy_command = poetry_command + [
        "mypy",
        project_folder,
        "--install-types",
        "--non-interactive",
        "--python-version",
        args.python_version,
    ]
    execute(*mypy_command)


if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument(
        "-p",
        "--python-version",
        default="3.12",
        help="Check the code assuming it will be running on Python x.y",
    )
    with curr_dir(project_folder):
        run(args.parse_args())
