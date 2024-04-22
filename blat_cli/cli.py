from typer import Typer

from blat_cli import DEFAULT_COMMANDS
from blat_cli.command import Command
from blat_cli.command import load_plugin_commands_from_settings


class BlatCLI(Typer):
    def register_command(self, command: Command):
        self.add_typer(command, name=command.name, help=command.description)


cli = BlatCLI(no_args_is_help=True)

for command in DEFAULT_COMMANDS:
    cli.register_command(command)

for plugin in load_plugin_commands_from_settings():
    cli.register_command(plugin)

if __name__ == "__main__":
    cli()
