import pytest
from src import configs
import playwright.sync_api as playwright


@pytest.fixture(scope="session")
def playwright_config() -> configs.PlaywrightConfig:
    return configs.PlaywrightConfig()


@pytest.fixture(scope="session")
def env_config() -> configs.EnvConfig:
    return configs.EnvConfig()


@pytest.fixture()
def playwright_browser(
    playwright_config: configs.PlaywrightConfig, env_config: configs.PlaywrightConfig
) -> playwright.Browser:
    with playwright.sync_playwright() as playwright_obj:
        browser: playwright.Browser
        if playwright_config.browser == "chromium":
            browser = playwright_obj.chromium.launch(
                channel=playwright_config.browser,
                headless=bool(playwright_config.headless),
                args=["--disable-gpu"],
                traces_dir=env_config.artifacts_dir,
            )
        else:
            raise SystemError(f"'{playwright_config.browser}' is not supported (yet)")

        try:
            yield browser
        finally:
            browser.close()
