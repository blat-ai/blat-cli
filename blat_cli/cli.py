from blat_cli import DEFAULT_COMMANDS
from blat_cli.command import Command
from blat_cli.command import load_plugin_commands_from_settings

plugins = []

for plugin in load_plugin_commands_from_settings():
    plugins.append(plugin)


class BlatCLI(Command):
    subcommands = [*DEFAULT_COMMANDS, *plugins]


cli = BlatCLI()

if __name__ == "__main__":
    cli()
