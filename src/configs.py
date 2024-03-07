import pydantic_settings
from typing import Optional


class PlaywrightConfig(pydantic_settings.BaseSettings):
    model_config = pydantic_settings.SettingsConfigDict(
        env_prefix="QA_PLAYWRIGHT_", env_file=".env", frozen=True, extra="ignore"
    )

    browser: str = ""
    headless: bool = True
    navigation_timeout_sec: int = 120
    elements_timeout_sec: int = 60


class EnvConfig(pydantic_settings.BaseSettings):
    model_config = pydantic_settings.SettingsConfigDict(
        env_prefix="QA_ENV_", env_file=".env", frozen=True, extra="ignore"
    )

    artifacts_dir: str = "artifacts/"
    url_ui: Optional[str] = None
