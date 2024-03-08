from src.page_object_models import base_pom


class MainPOM(base_pom.PageObjectModelBase):
    @property
    def default_url(self):
        return f"{self.env.url_ui}"

    def login(self):
        self.page.get_by_label("Cookie banner").click()
        self.page.get_by_test_id("bignav").get_by_role("link", name="Log in").click()
        self.page.get_by_placeholder("Enter your email").fill(self.env.user_name)
        self.page.get_by_placeholder("Enter your email").press("Enter")
        self.page.get_by_placeholder("Enter password").fill(self.env.user_password)
        self.page.get_by_role("button", name="Log in").click()
        self.page.wait_for_timeout(2000)
