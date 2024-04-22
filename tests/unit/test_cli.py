from blat_cli.cli import BlatCLI
from tests.conftest import FakeCommand


def test_blat_cli_has_registered_commands():
    command = FakeCommand()

    cli = BlatCLI()
    cli.register_command(command)

    assert command == cli.registered_groups[0].typer_instance
