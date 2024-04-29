import pytest
from typer.testing import CliRunner

from blat_cli.cli import cli


@pytest.fixture
def blat_cli():
    runner = CliRunner()

    def run_cli(*args):
        return runner.invoke(cli, args)

    return run_cli


def test_cli_help(blat_cli):
    result = blat_cli("--help")
    assert result.exit_code == 0
    assert "--help                        Show this message and exit." in result.output
