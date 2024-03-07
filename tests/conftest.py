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


@pytest.fixture()
def playwright_page(
    playwright_browser: playwright.Browser,
    playwright_config: configs.PlaywrightConfig,
    env_config: configs.EnvConfig,
) -> playwright.Page:
    browser_context = playwright_browser.new_context()

    new_page: playwright.Page = browser_context.new_page()

    with new_page as page:
        page.set_default_timeout(playwright_config.elements_timeout_sec * 1000)
        page.set_default_navigation_timeout(playwright_config.navigation_timeout_sec * 1000)

        yield page

    browser_context.close()
