import pytest
from typer.testing import CliRunner

from blat_cli import DEFAULT_COMMANDS
from blat_cli.cli import cli
from blat_cli.command import Command


@pytest.fixture
def blat_cli():
    runner = CliRunner()

    def run_cli(*args):
        return runner.invoke(cli, args)

    return run_cli


def test_cli_help(blat_cli):
    result = blat_cli("--help")
    assert result.exit_code == 0
    assert "Show this message and exit." in result.output
    for command in DEFAULT_COMMANDS:
        if isinstance(command, Command):
            assert command.name in result.output
        else:
            assert command.__name__.replace("_", "-") in result.output
