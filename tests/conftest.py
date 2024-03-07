import pytest
import sys
import pathlib
from datetime import datetime

sys.path.append(".")

from src import configs
import playwright.sync_api as playwright


@pytest.fixture(scope="session")
def playwright_config() -> configs.PlaywrightConfig:
    return configs.PlaywrightConfig()


@pytest.fixture(scope="session")
def env_config() -> configs.EnvConfig:
    return configs.EnvConfig()


@pytest.fixture(scope="session")
def session_timestamp() -> str:
    """Provides a session timestamp used in file names"""
    now = datetime.utcnow()
    return now.strftime("%Y%m%d%H%M%S")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """pytest hook that adds status for various stages of test execution

    Outcome test phase status into request.node.stash["status"].
    There are 3 different phases: "setup", "call" and "teardown".
    More information can be found at below link:
    https://docs.pytest.org/en/latest/example/simple.html#making-test-result-information-available-in-fixtures
    """
    outcome = yield
    rep = outcome.get_result()
    item.stash.setdefault("status", {})[rep.when] = rep.outcome
    return outcome


@pytest.fixture(scope="session", autouse=True)
def reporting_setup(env_config: configs.EnvConfig):
    if env_config.artifacts_remove_old:
        for file in pathlib.Path(env_config.artifacts_dir).rglob("*"):
            try:
                pathlib.Path(file).unlink(missing_ok=True)
            except PermissionError:
                pass


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
    request: pytest.FixtureRequest,
    playwright_browser: playwright.Browser,
    playwright_config: configs.PlaywrightConfig,
    env_config: configs.EnvConfig,
    session_timestamp: str,
) -> playwright.Page:
    browser_context = playwright_browser.new_context(record_video_dir=env_config.artifacts_dir)

    new_page: playwright.Page = browser_context.new_page()

    with new_page as page:
        page.set_default_timeout(playwright_config.elements_timeout_sec * 1000)
        page.set_default_navigation_timeout(playwright_config.navigation_timeout_sec * 1000)

        yield page

        video_path = pathlib.Path(page.video.path()) if page.video else None

    browser_context.close()

    try:
        test_status = request.node.stash["status"]["call"][:4]
    except KeyError:
        test_status = "unkn"
    artifact_file_name = (
        f"{env_config.artifacts_dir}{session_timestamp}_{test_status}_{request.node.name}"
    )

    if video_path and video_path.exists():
        new_video_path = f"{artifact_file_name}{video_path.suffix}"
        video_path.rename(new_video_path)
