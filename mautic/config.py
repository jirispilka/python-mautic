# -*- coding: utf-8 -*-
"""
    Set up the project constants here.
"""

from pathlib import Path

from pydantic import AnyUrl, Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppConfig(BaseSettings):

    CLIENT_ID: SecretStr | None = None
    CLIENT_SECRET: SecretStr | None = None

    BASE_URL: AnyUrl = Field(env="BASE_URL")

    USERNAME: str | None = None
    PASSWORD: SecretStr | None = None

    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent.parent / ".env", case_sensitive=True, extra="allow"
    )


Config = AppConfig()
