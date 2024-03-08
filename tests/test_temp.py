import logging
from src.page_object_models.trello_page import TrelloPage


def log() -> logging.Logger:
    return logging.getLogger(__name__)


def test_check_basic_columns(check, trello_page: TrelloPage):
    trello_page.main_pom.goto()
    trello_page.main_pom.login()
    trello_page.all_dashboards.goto()
    trello_page.all_dashboards.is_opened()
    trello_page.dashboard.goto()
    trello_page.dashboard.is_opened()
    with check:
        trello_page.dashboard.is_todo_visible()
    with check:
        trello_page.dashboard.is_doing_visible()
    with check:
        trello_page.dashboard.is_done_visible()
