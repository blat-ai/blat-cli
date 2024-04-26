from pathlib import Path
from typing import Tuple
from typing import Type

import typer
from pydantic import Field
from pydantic_settings import BaseSettings
from pydantic_settings import PydanticBaseSettingsSource
from pydantic_settings import SettingsConfigDict
from pydantic_settings import YamlConfigSettingsSource

app_dir = Path(typer.get_app_dir("blat"))


class Settings(BaseSettings):
    custom_plugins: list[str] = Field(
        description="List of class paths where the custom plugins are installed.", default=[]
    )
    blat_endpoint: str = Field(description="The API where the requests will be sent.", default="https://api.blat.ai")
    model_config = SettingsConfigDict(yaml_file=app_dir / "config")

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        return (env_settings, dotenv_settings, YamlConfigSettingsSource(settings_cls))


class Credentials(BaseSettings):
    api_key: str | None = Field(description="API key for the authentication to Blat APIs.", default=None)
    model_config = SettingsConfigDict(yaml_file=app_dir / "auth")

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        return (env_settings, dotenv_settings, YamlConfigSettingsSource(settings_cls))


settings = Settings()
credentials = Credentials()
