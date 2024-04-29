from importlib import reload

import pytest
import typer
from typer.testing import CliRunner

from blat_cli import settings


@pytest.fixture
def init_runner():
    import blat_cli.init.command as command

    reload(command)
    app = typer.Typer()
    app.command()(command.init)
    runner = CliRunner()

    def invoke(*args, **kwargs):
        return runner.invoke(app, *args, **kwargs)

    return invoke


def test_init_no_api_key(mocker, tmp_config, init_runner):
    install_pw_mock = mocker.patch("blat_cli.init.command.install_playwright")

    init_runner([], input="\n")

    install_pw_mock.assert_called_once_with(settings.playwright_dir)
    assert settings.Credentials.get_instance().api_key is None


def test_init_option_empty_api_key(mocker, tmp_config, init_runner):
    install_pw_mock = mocker.patch("blat_cli.init.command.install_playwright")

    init_runner(["--api-key", ""], input="\n")

    install_pw_mock.assert_called_once_with(settings.playwright_dir)
    assert settings.Credentials.get_instance().api_key is None


def test_init_option_api_key(mocker, tmp_config, init_runner):
    install_pw_mock = mocker.patch("blat_cli.init.command.install_playwright")

    init_runner(["--api-key", "1234"])

    install_pw_mock.assert_called_once_with(settings.playwright_dir)
    assert settings.Credentials.get_instance().api_key == "1234"
