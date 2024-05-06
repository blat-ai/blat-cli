import os
from pathlib import Path
from unittest.mock import MagicMock

from playwright.sync_api._generated import Page
from pydantic_core import Url

from blat_cli.client import Harvester
from blat_cli.harvester.command import generate
from blat_cli.harvester.command import obtain_content_and_url


def test_obtain_content_and_url(mocker):
    # Skip user confirmation for the shake of testing and emulate user interaction
    typer_mock = mocker.patch("blat_cli.harvester.command.typer")
    page_mock = MagicMock(spec=Page)
    page_mock.url = "https://www.iana.org/help/example-domains"
    page_mock.content.return_value = "<html><body><h1>Example Domains</h1></body></html>"
    browser_mock = mocker.patch("blat_cli.harvester.command.browser")
    browser_mock.return_value.__enter__.return_value = page_mock

    url, content = obtain_content_and_url("https://example.com/")

    typer_mock.confirm.assert_called_once()
    assert url == page_mock.url
    assert content == page_mock.content.return_value


def test_generate(mocker, tmpdir):
    json_schema = '{"type": "object"}'
    url = "https://example.com/"
    content = "<html><body><h1>Example Domains</h1></body></html>"
    file_content = b"content"

    mocker.patch("blat_cli.harvester.command.obtain_content_and_url", return_value=(url, content))
    client_mock = mocker.patch("blat_cli.harvester.command.client")
    client_mock.harvester_generate.return_value = Harvester(
        json_schema=json_schema,
        content=content,
        start_url=Url(url),
        file_content=file_content,
        file_name="harvester.zip",
    )

    generate(json_schema, url=url, output_path=Path(tmpdir))

    assert os.path.exists(Path(tmpdir) / "harvester.zip")
    with open(Path(tmpdir) / "harvester.zip", "rb") as f:
        assert f.read() == file_content

    os.remove(Path(tmpdir) / "harvester.zip")
