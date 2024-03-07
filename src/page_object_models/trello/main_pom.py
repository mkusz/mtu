from src.page_object_models import base_pom


class MainPOM(base_pom.PageObjectModelBase):
    @property
    def default_url(self):
        return f"{self.env.url_ui}"
