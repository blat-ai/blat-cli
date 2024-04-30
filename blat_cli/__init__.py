from typing import Any
from typing import Callable
from typing import List
from typing import Union

from blat_cli.command import Command
from blat_cli.harvester.command import command as harvester_command
from blat_cli.init.command import command as init_command
from blat_cli.init_system.command import command as init_system_command

DEFAULT_COMMANDS: List[Union[Callable[..., dict[Any, Any]], Command]] = [
    harvester_command,
    init_command,
    init_system_command,
]
