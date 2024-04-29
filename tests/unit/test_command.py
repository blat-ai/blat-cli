import inspect

from blat_cli.command import load_plugin_commands_from_settings
from blat_cli.settings import Settings
from tests.conftest import Fake
from tests.conftest import FakeCommand
from tests.conftest import fake_subcommand

command = FakeCommand()


def test_option_added():
    fake_option = Fake()

    fake_subcommand_with_option = fake_option.add_option(fake_subcommand)

    subcommand_signature = inspect.signature(fake_subcommand_with_option)
    assert subcommand_signature.parameters["foo"] == inspect.Parameter(
        name="foo", kind=inspect._ParameterKind.POSITIONAL_OR_KEYWORD, annotation=str
    )
    assert subcommand_signature.parameters["fake"] == inspect.Parameter(
        name="fake", kind=inspect._ParameterKind.POSITIONAL_OR_KEYWORD, annotation=int, default=1
    )
    assert subcommand_signature.return_annotation == dict[str, str]


def test_command_created():
    fake_command = FakeCommand()

    assert fake_command.name == "fake_command"
    assert len(fake_command.registered_commands) == 1
    subcommand = fake_command.registered_commands[0]
    subcommand_signature = inspect.signature(subcommand.callback)  # type: ignore
    assert subcommand_signature.parameters["foo"] == inspect.Parameter(
        name="foo", kind=inspect._ParameterKind.POSITIONAL_OR_KEYWORD, annotation=str
    )
    assert subcommand_signature.parameters["fake"] == inspect.Parameter(
        name="fake", kind=inspect._ParameterKind.POSITIONAL_OR_KEYWORD, annotation=int, default=1
    )
    assert subcommand_signature.return_annotation == dict[str, str]


def test_load_plugin_commands_from_settings(tmp_config):
    Settings.get_instance().custom_plugins = ["tests.unit.test_command"]
    plugins = list(load_plugin_commands_from_settings())

    assert len(plugins) == 1
    assert plugins[0] == command
