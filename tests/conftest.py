import pytest

from blat_cli import settings
from blat_cli.command import Command
from blat_cli.command import ReusableCommandOption


def fake_subcommand(foo: str) -> dict[str, str]:
    return {"foo": foo}


class Fake(ReusableCommandOption):
    annotation = int
    default_value = 1


class FakeCommand(Command):
    description = "Test command that does nothing"
    subcommands = [fake_subcommand]
    extra_options = [Fake()]


@pytest.fixture
def tmp_config(tmp_path, mocker, monkeypatch):
    mocker.patch("blat_cli.settings.app_dir", tmp_path)
    playwright_dir = tmp_path / "browsers"
    mocker.patch("blat_cli.settings.playwright_dir", playwright_dir)
    monkeypatch.setenv("PLAYWRIGHT_BROWSERS_PATH", str(playwright_dir))

    class MockCredentials(settings.Credentials):
        model_config = settings.SettingsConfigDict(yaml_file=tmp_path / "auth", validate_assignment=True)

    class MockSettings(settings.Settings):
        model_config = settings.SettingsConfigDict(yaml_file=tmp_path / "config", validate_assignment=True)

    mocker.patch("blat_cli.settings.Credentials.get_instance", return_value=MockCredentials())
    mocker.patch("blat_cli.settings.Settings.get_instance", return_value=MockSettings())
    return tmp_path
