import logging
from src.page_object_models import base_pom
from playwright.sync_api import expect
import allure


def log() -> logging.Logger:
    return logging.getLogger(__name__)


class DashboardPOM(base_pom.PageObjectModelBase):
    @property
    def default_url(self):
        return f"{self.env.url_ui}{self.env.dashboard}"

    def is_opened(self, selector: str = ""):
        expect(self.page.get_by_test_id("board-name-display")).to_have_text(
            self.env.dashboard_name
        )

    @allure.step("Check for todo")
    def is_todo_visible(self):
        log().debug("Check for todo")
        self.expect(
            locator=self.page.locator("h2").filter(has_text="Do zrobienia"),
        ).to_be_visible()

    def is_doing_visible(self):
        log().debug("Check for doing")
        self.expect(
            locator=self.page.locator("h2").filter(has_text="W trakcie"),
        ).to_be_visible()

    def is_done_visible(self):
        log().debug("Check for done")
        self.expect(
            self.page.locator("li").filter(has_text="done"),
        ).to_be_visible()
