import os
from pathlib import Path
from typing import Optional
from typing import Tuple
from typing import Type
from typing import TypeVar

import typer
import yaml
from pydantic import Field
from pydantic import model_validator
from pydantic_settings import BaseSettings as PydanticBaseSettings
from pydantic_settings import PydanticBaseSettingsSource
from pydantic_settings import SettingsConfigDict
from pydantic_settings import YamlConfigSettingsSource

from blat_cli.utils import PydanticSingleton

BaseSettingsType = TypeVar("BaseSettingsType", bound="BaseSettings")

app_dir = Path(typer.get_app_dir("blat"))
if not app_dir.exists():
    app_dir.mkdir(parents=True)
playwright_dir = app_dir / "browsers"
os.environ["PLAYWRIGHT_BROWSERS_PATH"] = str(playwright_dir)


class BaseSettings(PydanticBaseSettings, metaclass=PydanticSingleton):
    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[PydanticBaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        return (env_settings, dotenv_settings, YamlConfigSettingsSource(settings_cls))

    @model_validator(mode="after")
    def save_settings(self: BaseSettingsType) -> BaseSettingsType:
        """
        Saves the settings in the configuration file automatically every time the model is validated.
        """
        settings_file = self.model_config.get("yaml_file")
        if settings_file is not None:
            with open(str(settings_file), "w+") as f:
                f.write(yaml.dump(self.model_dump()))
        return self


class Settings(BaseSettings):
    model_config = SettingsConfigDict(yaml_file=app_dir / "config", validate_assignment=True)

    custom_plugins: list[str] = Field(
        description="List of class paths where the custom plugins are installed.", default=[]
    )
    blat_endpoint: str = Field(description="The API where the requests will be sent.", default="https://api.blat.ai")
    blat_client_timeout_s: int = Field(description="Timeout for the Blat client in seconds.", default=300)


class Credentials(BaseSettings):
    model_config = SettingsConfigDict(yaml_file=app_dir / "auth", validate_assignment=True)

    api_key: Optional[str] = Field(description="API key for the authentication to Blat APIs.", default=None)
