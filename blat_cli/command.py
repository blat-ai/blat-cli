import importlib
import inspect
import json
import logging
from enum import Enum
from itertools import chain
from itertools import groupby
from operator import attrgetter
from typing import Annotated
from typing import Any
from typing import Callable
from typing import Dict
from typing import Generator
from typing import Union

import yaml
from rich import print
from typer import Option
from typer import Typer

from blat_cli.settings import Settings
from blat_cli.utils import camel_to_snake_case


class ReusableCommandOption:
    annotation: Annotated[Any, Any]
    default_value: Any = None

    @property
    def name(self) -> str:
        return camel_to_snake_case(self.__class__.__name__)

    def pre_command(self, *args: Any, **kwargs: Any) -> None:
        """
        Hook to run code before the command is executed.
        """
        pass

    def post_command(self, command_output: Any, *args: Any, **kwargs: Any) -> None:
        """
        Hook to run code after the command is executed.
        """
        pass

    def _rebuild_signature(self, func: Callable[..., Any], wrapper: Callable[..., Any]) -> Callable[..., Any]:
        """
        Modifies the wrapper signature of the wrapper function to look like the original function and adds the option
        to the signature. This is required so that the option is picked by Typer and the help message is generated.
        """
        signature = inspect.signature(func)
        groups = {k: list(g) for k, g in groupby(signature.parameters.values(), attrgetter("kind"))}
        if not groups.get(inspect.Parameter.POSITIONAL_OR_KEYWORD):
            groups[inspect.Parameter.POSITIONAL_OR_KEYWORD] = []
        groups[inspect.Parameter.POSITIONAL_OR_KEYWORD] += [
            inspect.Parameter(
                self.name,
                inspect.Parameter.POSITIONAL_OR_KEYWORD,
                annotation=self.annotation,
                default=self.default_value,
            )
        ]
        for params in groups.values():
            if params:
                params.sort(key=lambda p: bool(p.default != inspect.Parameter.empty))
        parameters = sorted(chain(*(groups.values())), key=attrgetter("kind"))
        wrapper.__signature__ = signature.replace(parameters=parameters)  # type: ignore
        return wrapper

    def add_option(self, func: Callable[..., Any]) -> Callable[..., Any]:
        """
        Wraps the command function to add the option to the signature and call the pre and post hooks.
        """

        def wrapper(*args: list[Any], **kwargs: Dict[str, Any]) -> Any:
            option_value = kwargs.pop(self.name)
            self.pre_command(*args, **kwargs, **{self.name: option_value})
            command_output = func(*args, **kwargs)
            self.post_command(command_output, *args, **kwargs, **{self.name: option_value})

            return command_output

        return self._rebuild_signature(func, wrapper)


class Debug(ReusableCommandOption):
    annotation = Annotated[bool, Option(help="Enable debug mode", rich_help_panel="Output Options")]
    default_value = False

    def pre_command(self, *args: list[Any], **kwargs: Dict[str, Any]) -> None:
        """
        Sets the DEBUG level for ALL of the loggers in the application.
        """
        if kwargs.get(self.name, False):
            for name in logging.root.manager.loggerDict:
                logging.getLogger(name).setLevel(logging.DEBUG)


class OutputFormats(str, Enum):
    json = "json"
    yaml = "yaml"


class OutputFormat(ReusableCommandOption):
    annotation = Annotated[
        OutputFormats, Option(help="Format in which the output will be printed.", rich_help_panel="Output Options")
    ]
    default_value = OutputFormats.json

    def post_command(self, command_output: Any, *args: list[Any], **kwargs: Dict[str, Any]) -> None:
        """
        Prints the command output in the selected format.
        """
        if command_output:
            if kwargs.get(self.name, self.default_value) == OutputFormats.json:
                print(json.dumps(command_output))
            else:
                print(yaml.dump(command_output))


class Command(Typer):
    description: str
    subcommands: list[Union[Callable[..., dict[Any, Any]], "Command"]] = []
    extra_options: list[ReusableCommandOption] = [OutputFormat(), Debug()]

    @property
    def name(self) -> str:
        return camel_to_snake_case(self.__class__.__name__)

    def __init__(self, *args: Any, **kwargs: Any):
        kwargs["no_args_is_help"] = True
        super().__init__(*args, **kwargs)
        self._register_subcommands()

    def _register_subcommands(self) -> None:
        for subcommand in self.subcommands:
            if isinstance(subcommand, Command):
                self.add_typer(subcommand, name=subcommand.name, help=subcommand.description)
            else:
                self.command(name=subcommand.__name__.replace("_", "-"), help=subcommand.__doc__)(
                    self._add_extra_options(subcommand)
                )

    def _add_extra_options(self, func: Callable[..., Any]) -> Callable[..., Any]:
        for option in self.extra_options:
            func = option.add_option(func)

        return func


def load_plugin_commands_from_settings() -> Generator[Command, None, None]:
    """
    Load the custom plugins from the settings.
    """
    custom_plugins = Settings().custom_plugins
    for plugin in custom_plugins:
        module = importlib.import_module(plugin)
        yield module.command
