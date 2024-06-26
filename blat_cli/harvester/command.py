import contextlib
import os
from pathlib import Path
from typing import Annotated
from typing import Any
from typing import Generator
from typing import Optional
from typing import Tuple

import typer
from playwright.sync_api import sync_playwright
from playwright.sync_api._generated import Page
from rich.console import Console
from rich.progress import Progress
from rich.progress import SpinnerColumn
from rich.progress import TextColumn

from blat_cli.client import BlatClient
from blat_cli.command import Command
from blat_cli.settings import Credentials
from blat_cli.settings import Settings

console = Console()
client = BlatClient(
    Settings().blat_endpoint, client_timeout_s=Settings().blat_client_timeout_s, api_key=Credentials().api_key
)


@contextlib.contextmanager
def browser(url: Optional[str] = None, **kwargs: Any) -> Generator[Page, None, None]:
    pw = sync_playwright().start()
    browser = pw.chromium.launch(**kwargs)
    page = browser.new_page()
    if url:
        page.goto(url)

    yield page

    browser.close()


def obtain_content_and_url(url: Optional[str] = None) -> Tuple[str, str]:
    console.print("A browser will open. Please navigate to the page where the data is located and visible.")
    with browser(url, headless=False) as page:
        typer.confirm("Is the data visible in the browser?", default=True, abort=True, show_default=True)
        content = page.content()
        url = page.url

    return url, content


def generate(
    schema: Annotated[str, typer.Option(help="The JSON Schema to generate the Harvester.")],
    output_path: Annotated[
        Path, typer.Option(help="The path where the zip_file will be stored", default_factory=os.getcwd)
    ],
    url: Annotated[Optional[str], typer.Option(help="The URL where the data is located.")] = None,
) -> dict[Any, Any]:
    """
    Generates a Harvester using Blat AI technology and downloads a zip file with the generated code
    for the given schema and URL.
    """
    url, content = obtain_content_and_url(url)
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:
        progress.add_task(description=f"Generating your Harvester for {url}...", total=None)
        harvester = client.harvester_generate(schema, content, url)
        file_path = output_path / (harvester.file_name or "harvester.zip")

        with open(file_path, "wb") as f:
            f.write(harvester.file_content)

    console.print(f"Harvester generated successfully! You can find it in {str(file_path)}", style="bold green")
    return {}


class Harvester(Command):
    description = "Command that manages Blat Harvesters"
    subcommands = [generate]


command = Harvester()
