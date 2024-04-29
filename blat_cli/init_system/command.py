import subprocess

from playwright._impl._driver import compute_driver_executable
from playwright._impl._driver import get_driver_env
from rich.console import Console
from rich.progress import Progress
from rich.progress import SpinnerColumn
from rich.progress import TextColumn

console = Console()


def install_playwright_system_dependencies():
    driver_executable = compute_driver_executable()
    env = get_driver_env()
    args = [str(driver_executable), "install-deps"]
    completed_process = subprocess.run(args, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    completed_process.check_returncode()


def init_system():
    """
    Installs the system dependencies required by Blat CLI.
    """
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:
        progress.add_task(description="Installing the dependencies...", total=None)
        install_playwright_system_dependencies()

    console.print("Blat CLI system dependencies installed successfully! \U0001F680", style="bold green")

    return {}


command = init_system
