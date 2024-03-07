import logging
from src.page_object_models.trello_pom import TrelloPOM


def log() -> logging.Logger:
    return logging.getLogger(__name__)


def test_temp_open_trello(trello_page: TrelloPOM):
    trello_page.main_pom.goto()
