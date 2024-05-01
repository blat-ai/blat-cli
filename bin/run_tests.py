import argparse
import os
import subprocess
from contextlib import contextmanager
from os import path

project_folder = path.dirname(path.dirname(path.abspath(__file__)))
tests_folder = path.join(project_folder, "tests")


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
    Executes the tests of the project using the given arguments.

    :param args: The arguments to use to run the tests.
    """
    command_args = ["poetry", "run", "pytest"]
    if args.with_cov:
        command_args.append("--cov=blat_cli")
        command_args.append("--cov-report xml")
        command_args.append("--cov-fail-under 80")
    command_args.extend(args.test_dirs)
    execute(*command_args)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "test_dirs",
        default=["unit/", "integration/"],
        nargs="*",
        help="One or more directories containing tests.",
    )
    parser.add_argument(
        "-c",
        "--with-cov",
        default=False,
        action="store_true",
        help="Run default test-runner with code coverage enabled.",
    )
    with curr_dir(tests_folder):
        run(parser.parse_args())
