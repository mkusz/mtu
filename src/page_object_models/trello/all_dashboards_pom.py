from src.page_object_models import base_pom


class AllDashboardsPOM(base_pom.PageObjectModelBase):
    @property
    def default_url(self):
        return f"{self.env.url_ui}{self.env.all_dashboards}"

    def is_opened(self, selector: str = ""):
        self.page.wait_for_url(self.default_url)
