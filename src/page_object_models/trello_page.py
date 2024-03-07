import playwright.sync_api as playwright
from src.page_object_models.trello import main_pom


class TrelloPage:
    def __init__(self, page: playwright.Page):
        self.main_pom = main_pom.MainPOM(page=page)
