import logging
import urllib.parse
from typing import Optional

import playwright.sync_api as playwright

from src import configs


def _logger() -> logging.Logger:
    return logging.getLogger(__name__)


class PageObjectModelBase:
    def __init__(self, page: playwright.Page):
        self.page: playwright.Page = page
        self.env: configs.EnvConfig = configs.EnvConfig()
        self.playwright: configs.PlaywrightConfig = configs.PlaywrightConfig()

    @property
    def default_url(self):
        """Returns default url of the given web page"""
        raise NotImplementedError

    def is_opened(self, selector: str):
        """Check is given POM opened (have to implemented inside given POM)"""
        raise NotImplementedError

    def goto(self, params: Optional[dict] = None):
        if params:
            url_params = urllib.parse.urlencode(params)
            url = f"{self.default_url}?{url_params}"
        else:
            url = self.default_url
        _logger().debug(f"Go to: {url}")
        self.page.goto(url)
