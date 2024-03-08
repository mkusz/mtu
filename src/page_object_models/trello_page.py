import playwright.sync_api as playwright
from src.page_object_models.trello import main_pom
from src.page_object_models.trello import dashboard_pom
from src.page_object_models.trello import all_dashboards_pom


class TrelloPage:
    def __init__(self, page: playwright.Page):
        self.main_pom = main_pom.MainPOM(page=page)
        self.all_dashboards = all_dashboards_pom.AllDashboardsPOM(page=page)
        self.dashboard = dashboard_pom.DashboardPOM(page=page)
