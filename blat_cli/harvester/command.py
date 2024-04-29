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
from rich import print

from blat_cli.client import BlatClient
from blat_cli.command import Command
from blat_cli.settings import Credentials
from blat_cli.settings import Settings

client = BlatClient(Settings.get_instance().blat_endpoint, Credentials.get_instance().api_key)


@contextlib.contextmanager
def browser(url: Optional[str] = None, **kwargs) -> Generator[Page, None, None]:
    pw = sync_playwright().start()
    browser = pw.chromium.launch(**kwargs)
    page = browser.new_page()
    if url:
        page.goto(url)

    yield page

    browser.close()


def obtain_content_and_url(url: Optional[str] = None) -> Tuple[str, str]:
    print("A browser will open. Please navigate to the page where the data is located and visible.")
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
    harvester = client.harvester_generate(schema, content, url)
    file_path = output_path / (harvester.file_name or "harvester.zip")

    with open(file_path, "wb") as f:
        f.write(harvester.file_content)

    return {"schema": schema, "url": url, "file_path": file_path}


class Harvester(Command):
    description = "Command that manages Blat Harvesters"
    subcommands = [generate]


command = Harvester()
