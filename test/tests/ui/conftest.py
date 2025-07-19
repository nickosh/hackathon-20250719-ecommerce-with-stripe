import pytest
from playwright.sync_api import Page

from pages.main import MainPage


@pytest.fixture(autouse=True)
def test_page(page: Page):
    test_page = MainPage(page)
    test_page.navigate()
    yield test_page
