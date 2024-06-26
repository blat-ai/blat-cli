import subprocess
from pathlib import Path
from typing import Annotated
from typing import Any
from typing import Optional

import typer
from playwright._impl._driver import compute_driver_executable
from playwright._impl._driver import get_driver_env
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress
from rich.progress import SpinnerColumn
from rich.progress import TextColumn

from blat_cli.settings import Credentials
from blat_cli.settings import playwright_dir

console = Console()


def install_playwright(install_path: Path) -> None:
    driver_executable = compute_driver_executable()
    env = get_driver_env()
    env["PLAYWRIGHT_BROWSERS_PATH"] = str(install_path)
    args = [str(driver_executable), "install", "chromium"]
    completed_process = subprocess.run(args, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    completed_process.check_returncode()


def init(
    api_key: Annotated[Optional[str], typer.Option(help="The API Key to access Blat endpoints")] = None,
) -> dict[Any, Any]:
    """
    Install the dependencies and initialize the Blat CLI configuration.
    """
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:
        progress.add_task(description="Installing the dependencies...", total=None)
        install_playwright(playwright_dir)

    if not api_key:
        api_key = typer.prompt(
            "Which is your API key? (You can skip this step and add it later in the config file)",
            hide_input=True,
            default="",
        )
    if api_key:
        Credentials().api_key = api_key  # Save the API key in the configuration file.

    console.print("Remember to execute the following command if you haven't done it yet:")
    console.print(Panel("$ sudo blat init-system", expand=True), style="")
    console.print("Blat CLI initialized succesfully!", style="bold green")

    return {}


command = init
