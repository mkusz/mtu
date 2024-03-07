import pydantic_settings


class PlaywrightConfig(pydantic_settings.BaseSettings):
    model_config = pydantic_settings.SettingsConfigDict(
        env_prefix="QA_PLAYWRIGHT_",
        env_file=".env",
        frozen=True,
    )

    browser: str = ""
    headless: bool = True
