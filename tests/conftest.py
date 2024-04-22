from blat_cli.command import Command
from blat_cli.command import ReusableCommandOption


def fake_subcommand(foo: str) -> dict[str, str]:
    return {"foo": foo}


class Fake(ReusableCommandOption):
    annotation = int
    default_value = 1


class FakeCommand(Command):
    description = "Test command that does nothing"
    subcommands = [fake_subcommand]
    extra_options = [Fake()]
