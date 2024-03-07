import pytest
from src import configs


@pytest.fixture(scope="session")
def playwright_config() -> configs.PlaywrightConfig:
    return configs.PlaywrightConfig()
